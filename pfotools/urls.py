from django.conf.urls import patterns, include, url
from django.contrib import admin

from pfotools.views import Index

import pfodb

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pfotools.views.home', name='home'),
    url(r'^$', Index.as_view(), name='index'),

    url(r'^pfodb/', include(pfodb.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
