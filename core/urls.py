from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^album/(?P<slug>\d+)/contributor/?', 'views_contributoralbum.entrance', name='resource_contributoralbum'),
    url(r'^album/(?P<slug>\d+)?/?', 'views_album.entrance', name='resource_album'),
)
