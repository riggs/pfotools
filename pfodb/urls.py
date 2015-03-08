# -*- coding: utf-8 -*-

from django.conf.urls import include, patterns, url

from . import views
from . import rest_api

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pfotools.views.home', name='home'),
    url(r'^$', views.Industry_Index.as_view(), name='industry_index'),
    url(r'''^crafting/?((?<=/)(?P<query>[\w ']+))?$''', views.Item.as_view(), name='items'),
    url(r'''^refining/?((?<=/)(?P<query>[\w ']+)(\+(?P<plus_value>\d))?)?$''',
        views.Component.as_view(), name='components'),
    url(r'^api/', include(rest_api.generate_urls('api'), namespace='api', app_name='pfodb')),
)

