from django.conf.urls import patterns, include, url
#from core import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'galbum.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/', include("core.urls")),
    url(r'^admin/', include(admin.site.urls)),
)
