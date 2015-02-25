
from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pfotools.views.home', name='home'),
    url(r'^$', Industry_Index.as_view(), name='industry_index'),
    url(r'''^crafting(/(?P<query>[\w ']+))?$''', Item.as_view(), name='items'),
    #url(r'''^crafting(/(?P<query>[\w ']+)(\w+\+(?P<plus_value>\d))?)?$''', Item.as_view(), name='items'),
    url(r'''^refining(/(?P<query>[\w ']+))?$''', Component.as_view(), name='items'),
    #url(r'''^refining(/(?P<query>[\w ']+)(\w+\+(?P<plus_value>\d))?)?$''', Component.as_view(), name='items'),
)