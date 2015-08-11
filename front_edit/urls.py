from __future__ import unicode_literals
from django.conf.urls import url
from .views import front_end_update_view

urlpatterns = [
    url(r'^ft_edit/(?P<app_label>[^/]+)/(?P<model_name>[^/]+)/(?P<pk>\d+)/$',
        front_end_update_view, name='ft_edit'),
]
