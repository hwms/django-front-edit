from __future__ import unicode_literals
from uuid import UUID, uuid5
from bs4 import BeautifulSoup as BS

from django.template import Context
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse, NoReverseMatch
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.safestring import mark_safe
from django.utils.importlib import import_module
from django.utils.functional import lazy
from django.conf import settings

from classytags.core import Tag, Options
from classytags.helpers import InclusionTag
from classytags.arguments import Argument

from ...forms import make_form
from ... import DEFER

from . import register
from .arguments import NonGreedyMultiValueArgument

CP_ERROR = ("Edit tags require the use of the context processor included with "
    "this app. Add front_edit.context_processors.edit_defer to your context "
    "processors list in your settings.py file.")
CF_IMPORT_ERROR = ("Could not import the custom field: {}: {}")
CF_FIELD_ERROR = ("Could not access the media on the form field widget "
    "for: {}: {}")
MM_ERROR = ("Can only edit one model per block. Attempted to edit both {} "
    "and {}.")
ST_LOGOUT_ERROR = ("Set FRONT_EDIT_LOGOUT_URL_NAME to the url name of your logout "
    "view in your settings.py file: {}")

MEDIA = []
for field_path in settings.FRONT_EDIT_CUSTOM_FIELDS:
    try:
        module_path, field_name = field_path.rsplit('.', 1)
        module = import_module(module_path)
        field = getattr(module, field_name)
    except (ValueError, ImportError, AttributeError) as e:
        raise ImportError(CF_IMPORT_ERROR.format(field_path, e))
    try:
        MEDIA.append(field().formfield().widget.media)
    except AttributeError as e:
        raise ImproperlyConfigured(CF_FIELD_ERROR.format(field_path, e))

@register.tag
class Edit(Tag):
    options = Options(
        NonGreedyMultiValueArgument('models_fields', resolve=False),
        Argument('edit_class', default=None, required=False),
        blocks=[('endedit', 'nodelist')],
    )

    def render_tag(self, context, models_fields, edit_class, nodelist):
        # is this thing on?
        user = context['user']
        if not user.is_staff or not settings.FRONT_EDIT_INLINE_EDITING_ENABLED:
            return nodelist.render(context)

        # make uuid stuff and check configuration
        try:
            uuid = UUID(int=len(context[DEFER]))
        except (KeyError, ValueError):
            raise ImproperlyConfigured(CP_ERROR)
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
        output = unicode(nodelist.render(context))#.strip('\r\n').strip()
        context.pop()

        # get the id, or insert id, or wrap the whole thing
        soup = BS(output)
        parent = None
        if soup.body:
            parent = soup.body
            root = soup.body.next
        elif soup.html:
            parent = soup.html
            root = soup.html.next
        else:
            root = soup

        if root.findNextSibling() is not None:
            if parent is not None:
                parent.name = 'div'
                parent['class'] = 'editable'
                root = parent
            else:
                new = soup.new_tag('div', **{"class":"editable"})
                new.append(root)
                root = new

        try:
            editable_id = root['id']
        except KeyError:
            editable_id = str(uuid5(uuid, uuid_name))
            root['id'] = editable_id

        context[DEFER].append(dict(
            model=model,
            fields=fields,
            editable_id=editable_id,
            edit_class=edit_class,
        ))
        return mark_safe(unicode(root))

@register.tag
class EditLoader(InclusionTag):

    def get_template(self, context, **kwargs):
        """
        Returns the template to be used for the current context and arguments.
        """
        return settings.FRONT_EDIT_LOADER_TEMPLATE

    @staticmethod
    def _make_toolbar(context):
        try:
            editable_obj = context['editable_obj']
        except KeyError:
            editable_obj = None
        try:
            logout_url=reverse(settings.FRONT_EDIT_LOGOUT_URL_NAME)
        except NoReverseMatch as e:
            raise ImproperlyConfigured(ST_LOGOUT_ERROR.format(e))
        return render_to_string(settings.FRONT_EDIT_TOOLBAR_TEMPLATE,
            dict(
                editable_obj=editable_obj,
                logout_url=logout_url,
                REDIRECT_FIELD_NAME=REDIRECT_FIELD_NAME
            ), context)

    @staticmethod
    def _make_editables(context, deferred):
        editables = []
        for defer in deferred:
            model = defer['model']
            editables.append(render_to_string(
                settings.FRONT_EDIT_EDITABLE_TEMPLATE, dict(
                    form_for_fields=make_form(model.__class__, defer['fields'])(
                        instance=model),
                    editable_id=defer['editable_id'],
                    app_label=model._meta.app_label,
                    model_name=model.__class__.__name__.lower(),
                    pk=model.pk,
                    edit_class=defer['edit_class'],
                ), context))
        return editables

    def get_context(self, context):
        user = context['user']
        if user.is_staff and settings.FRONT_EDIT_INLINE_EDITING_ENABLED:
            try:
                context['editables'] = self._make_editables(context,
                    context[DEFER])
            except (KeyError, ValueError):
                raise ImproperlyConfigured(CP_ERROR)
            context['media'] = MEDIA
            context['toolbar'] = EditLoader._make_toolbar(context)
        return context
