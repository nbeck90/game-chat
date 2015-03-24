from django.conf.urls import patterns, url

urlpatterns = patterns('profiles.views',
    url(r'^profile/(?P<slug>[\w\-]+)/$', 'profile', name='profile'),
    url(r'^profile/edit$', 'ProfileEdit', name='profile_edit')
)
