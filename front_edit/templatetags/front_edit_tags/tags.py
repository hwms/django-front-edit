from __future__ import unicode_literals
import sys
import re
import base64
from uuid import UUID, uuid5
from copy import copy
from importlib import import_module

from django.template import Context
from django.template.base import NodeList, TextNode
from django.template.loader import render_to_string
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse, NoReverseMatch
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe
from django.utils.functional import lazy
from django.utils.html import format_html

from bs4 import BeautifulSoup

from classytags.core import Tag, Options
from classytags.helpers import InclusionTag
from classytags.arguments import Argument

from front_edit.compat import str, range, chr
from front_edit.forms import make_form
from front_edit.settings import appsettings
from front_edit.utils import OrderedSet

from . import register
from .arguments import NonGreedyMultiValueArgument


CP_ERROR = ("Edit tags require the use of the context processor included with "
            "this app. Add front_edit.context_processors.edit_defer to your "
            "context processors list in your settings.py file.")
CF_IMPORT_ERROR = ("Could not import the custom field: {}: {}")
CF_FIELD_ERROR = ("Could not access the media on the form field widget "
                  "for: {}: {}")
MM_ERROR = ("Can only edit one model per block. Attempted to edit both {} "
            "and {}.")
ST_LOGOUT_ERROR = ("Set FRONT_EDIT_LOGOUT_URL_NAME to the url name of your "
                   "logout view in your settings.py file: {}")
ST_PARSER_ERROR = ("'django-front-edit' is incompatible with 'html.parser', "
                   "please set FRONT_EDIT_HTML_PARSER to 'html5lib' (default) "
                   "or 'lxml' in your settings.py file.")

MEDIA = []
for field_path in appsettings.CUSTOM_FIELDS:
    try:
        module_path, field_name = field_path.rsplit('.', 1)
        module = import_module(module_path)
        field = getattr(module, field_name)
    except (ValueError, ImportError, AttributeError) as e:
        raise ImportError(CF_IMPORT_ERROR.format(field_path, e))
    try:
        MEDIA.append(str(field().formfield().widget.media))
    except AttributeError as e:
        raise ImproperlyConfigured(CF_FIELD_ERROR.format(field_path, e))

def BS(html):
    if appsettings.HTML_PARSER == 'html.parser':
        raise ImproperlyConfigured(ST_PARSER_ERROR)
    return BeautifulSoup(html, appsettings.HTML_PARSER)

def edit(context, models_fields, edit_class, nodelist):
    # is this thing on?
    user = context['user']
    if not is_enabled(user):
        return nodelist.render(context)

    # make uuid stuff and check configuration
    uuid = get_uuid(context)
    uuid_name = ','.join(models_fields)

    # get the model and fields
    model = None
    fields = []
    for model_field in models_fields:
        class_name, field = model_field.split('.')
        if model is None:
            model = context[class_name]
        elif model != context[class_name]:
            raise Exception(MM_ERROR.format(model, context[class_name]))
        # check if field exists
        getattr(model, field)
        fields.append(field)

    if not user.has_perm('{}.change_{}'.format(model._meta.app_label,
                                               model._meta.model_name)):
        return nodelist.render(context)

    context.push()
    output = str(nodelist.render(context))
    context.pop()

    root = bs_root(output)

    try:
        editable_id = root['id']
    except KeyError:
        editable_id = str(uuid5(uuid, uuid_name))
        root['id'] = editable_id

    context[appsettings.DEFER_KEY].append(dict(
        model=model,
        fields=fields,
        editable_id=editable_id,
        edit_class=edit_class,
        admin_url='',
    ))

    return mark_safe(str(root))

def edit_link(context, admin_url, edit_class, nodelist):
    # is this thing on?
    user = context['user']
    if not is_enabled(user):
        return nodelist.render(context)

    # make uuid stuff and check configuration
    uuid = get_uuid(context)
    uuid_name = admin_url

    context.push()
    output = str(nodelist.render(context))
    context.pop()

    root = bs_root(output)

    try:
        editable_id = root['id']
    except KeyError:
        editable_id = str(uuid5(uuid, uuid_name))
        root['id'] = editable_id

    context[appsettings.DEFER_KEY].append(dict(
        model=None,
        fields=[],
        editable_id=editable_id,
        edit_class=edit_class,
        admin_url=admin_url,
    ))

    return mark_safe(str(root))

if appsettings.USE_HINTS:
    VKEY = appsettings.VIGENERE_KEY

    if VKEY is None:
        ENCODE = lambda clear: clear
        DECODE = lambda enc: enc
    else:
        VKEY = str(VKEY)
        LVKEY = len(VKEY)

        UNILIMIT = sys.maxunicode

        ENCODE = lambda clear: base64.b64encode(
            ''.join([chr((ord(c) + ord(VKEY[i % LVKEY])) % UNILIMIT)
                     for i, c in enumerate(clear)]).encode('utf-8'))

        DECODE = lambda enc: ''.join([
            chr((UNILIMIT + ord(e) - ord(VKEY[i % LVKEY])) % UNILIMIT)
            for i, e in enumerate(base64.b64decode(enc).decode('utf-8'))])

    @register.tag
    class EditHint(Tag):
        options = Options(
            Argument('instance'),
            Argument('fields'),
            Argument('edit_class', default=None, required=False),
        )
        def render_tag(self, context, instance, fields, edit_class):
            ct_id = ContentType.objects.get_for_model(instance).id
            id = instance.id
            hint = ENCODE('{}:{}:{}:{}'.format(ct_id, id, fields,
                                               edit_class or ''))
            return format_html('data-hint="{}"', hint)

    @register.tag
    class EditWithHints(Tag):
        non_greedy_all = re.compile(".*")
        options = Options(
            blocks=[('endedit_with_hints', 'nodelist')],
        )

        def render_tag(self, context, nodelist):
            html = nodelist.render(context)
            user = context['user']
            if not user.is_staff or not appsettings.INLINE_EDITING_ENABLED:
                return html
            soup = BS(html)
            ctx = {}
            models_fields = []
            new_nodelists = []
            results = soup.findAll('div', {'data-hint' : self.non_greedy_all})
            for idx, result in enumerate(results):
                hint = result.attrs['data-hint']

                ct_id, id, fields, edit_class = DECODE(hint).split(':')
                fields = fields.split(',')

                model_class = ContentType.objects.get(id=ct_id).model_class()
                instance = model_class.objects.get(id=id)

                name = '__front_edit_{}'.format(idx)
                ctx[name] = instance

                models_field = []
                for field in fields:
                    models_field.append('{}.{}'.format(name, field))
                models_fields.append(models_field)

                new_nodelist = NodeList()
                new_nodelist.append(TextNode(str(result)))
                new_nodelists.append(new_nodelist)

            outputs = []
            context.update(ctx)
            for i in range(len(new_nodelists)):
                output = edit(context, models_fields[i], '', new_nodelists[i])
                outputs.append(output)
            context.pop()
            return mark_safe(''.join(outputs))

@register.tag
class Edit(Tag):
    options = Options(
        NonGreedyMultiValueArgument('models_fields', resolve=False),
        Argument('edit_class', default=None, required=False),
        blocks=[('endedit', 'nodelist')],
    )

    def render_tag(self, context, models_fields, edit_class, nodelist):
        return edit(context, models_fields, edit_class, nodelist)

@register.tag
class EditLink(Tag):
    options = Options(
        Argument('admin_url'),
        Argument('edit_class', default=None, required=False),
        blocks=[('endedit_link', 'nodelist')],
    )

    def render_tag(self, context, admin_url, edit_class, nodelist):
        return edit_link(context, admin_url, edit_class, nodelist)

@register.tag
class EditLoader(InclusionTag):
    def __init__(self, *args, **kwargs):
        super(EditLoader, self).__init__(*args, **kwargs)
        self.media = OrderedSet(copy(MEDIA))

    def get_template(self, context, **kwargs):
        """
        Returns the template to be used for the current context and arguments.
        """
        return appsettings.LOADER_TEMPLATE

    @staticmethod
    def _make_toolbar(context):
        try:
            editable_obj = context['editable_obj']
        except KeyError:
            editable_obj = None
        try:
            logout_url = reverse(appsettings.LOGOUT_URL_NAME)
        except NoReverseMatch as e:
            raise ImproperlyConfigured(ST_LOGOUT_ERROR.format(e))
        return render_to_string(appsettings.TOOLBAR_TEMPLATE,
            dict(editable_obj=editable_obj, logout_url=logout_url,
                 REDIRECT_FIELD_NAME=REDIRECT_FIELD_NAME), context)

    def _make_editables(self, context, deferred):
        editables = []
        for defer in deferred:
            admin_url = defer['admin_url']
            model = defer['model']
            subcontext = {
                'editable_id': defer['editable_id'],
                'edit_class': defer['edit_class'],
                'admin_url': admin_url,
            }

            if model != None:
                model_class = model.__class__
                form_for_fields = make_form(model_class, defer['fields'])(
                    instance=model, auto_id='{}_%s'.format(defer['editable_id']))
                try:
                    self.media.add(str(form_for_fields.media))
                except AttributeError:
                    pass
                if model._deferred:
                    model_name = model_class.__base__.__name__.lower()
                else:
                    model_name = model_class.__name__.lower()

                subcontext.update({
                    'form_for_fields': form_for_fields,
                    'app_label': model._meta.app_label,
                    'model_name': model_name,
                    'pk': model.pk,
                })

            editables.append(render_to_string(
                appsettings.EDITABLE_TEMPLATE, subcontext, context))

        return editables

    def get_context(self, context):
        user = context['user']
        if user.is_staff and appsettings.INLINE_EDITING_ENABLED:
            try:
                context['editables'] = self._make_editables(
                    context, context[appsettings.DEFER_KEY])
            except (KeyError, ValueError):
                raise ImproperlyConfigured(CP_ERROR)
            context['jquery_backup'] = appsettings.JQUERY_BACKUP
            context['jquery_builtin'] = appsettings.JQUERY_BUILTIN
            context['jquery_cdn'] = appsettings.JQUERY_CDN
            context['jquery_version'] = appsettings.JQUERY_VERSION
            context['media'] = list(self.media)
            context['toolbar'] = EditLoader._make_toolbar(context)
        return context


def is_enabled(user):
    return user.is_staff and appsettings.INLINE_EDITING_ENABLED

def get_uuid(context):
    try:
        return UUID(int=len(context[appsettings.DEFER_KEY]))
    except (KeyError, ValueError):
        raise ImproperlyConfigured(CP_ERROR)

def bs_root(template_html):
    """Get the id, or insert id, or wrap the whole thing"""
    soup = BS(template_html)
    parent = None
    if soup.body:
        parent = soup.body
        root = soup.body.next
    elif soup.html:
        parent = soup.html
        root = soup.html.next
    else:
        root = soup

    if root is None:
        # not sure what you're expecting us to do, you gave us nothing
        root = soup.new_tag('div', **{"class":"editable"})
    elif root.findNextSibling() is not None:
        # we are not alone in here
        if parent is not None:
            # set parent as root
            parent.name = 'div'
            parent['class'] = 'editable'
            root = parent
        else:
            # make a new parent
            new = soup.new_tag('div', **{"class":"editable"})
            new.append(root)
            root = new
    return root
