from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^album/(?P<slug>\d+)/contributors/?(?P<username>\w+)?/?', 'core.views_contributoralbum.entrance', name='resource_contributoralbum'),
    url(r'^album/(?P<slug>\d+)/mobjects/?', 'core.views_mobject.entrance', name='resource_mobject'),
    url(r'^album/(?P<slug>\d+)?/?', 'core.views_album.entrance', name='resource_album'),    
    
    url(r'^contributor/(?P<username>\w+)?/?', 'core.views_contributor.entrance', name='resource_contributor'),
    
    
)
