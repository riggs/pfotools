from django.conf.urls import patterns, include, url
from django.contrib import admin

from pfotools.views import Index

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pfotools.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', Index.as_view(), name='index'),

    url(r'^admin/', include(admin.site.urls)),
)



