
from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pfotools.views.home', name='home'),
    url(r'^$', Industry_Index.as_view(), name='industry_index'),
    url(r'^/items/(?P<query>\w+)/(?P<plus_value>\w+)$', Item.as_view(), name='items'),
)