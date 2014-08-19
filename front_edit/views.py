from __future__ import unicode_literals
from future.builtins import str

from json import dumps as json_dumps

from django import http
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

from .forms import make_form

def try_cast_or_404(cast_type, input):
    ''' Used for GET variables i.e. when you expect to receive an int
        returns 404 if the cast is unsuccessful
    '''
    assert(isinstance(cast_type,type))
    try:
        if input is None:
            raise ValueError
        return cast_type(input)
    except (ValueError, TypeError):
        raise http.Http404

@never_cache
@require_http_methods(('POST', 'PUT'))
@login_required
@user_passes_test(lambda u:u.is_staff)
def front_end_update_view(request, *args, **kwargs):
    if request.is_ajax():
        user = request.user

        app_label = try_cast_or_404(str, kwargs.get('app_label', None))
        model_name = try_cast_or_404(str, kwargs.get('model_name', None))

        if not user.has_perm('{}.change_{}'.format(app_label, model_name)):
            return http.HttpResponseForbidden()

        pk = try_cast_or_404(str, kwargs.get('pk', None))
        fields = try_cast_or_404(str, request.POST.get('form_fields', None))
        model = ContentType.objects.get(app_label=app_label,
            model=model_name).model_class()

        form_class = make_form(model, fields.split(','))
        try:
            form = form_class(instance=model.objects.get(pk=pk),
                data=request.POST)
        except model.DoesNotExist:
            raise http.Http404()
        valid = form.is_valid()
        if valid:
            form = form_class(instance=form.save())

        kwargs.update(
            valid=valid,
            form=render_to_string('front_edit/includes/form.html', dict(
                form_for_fields=form,
                app_label=app_label,
                model_name=model_name,
                pk=pk), RequestContext(request))
        )
        response_kwargs = dict(
            content_type='application/json'
        )
        return http.HttpResponse(json_dumps(kwargs), **response_kwargs)
    return http.HttpResponseBadRequest()
