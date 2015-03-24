from django.conf.urls import patterns, url

urlpatterns = patterns('profiles.views',
    url(r'^$', 'profile', name='profile'),
    url(r'^(?P<slug>[\w\-]+)/$', 'other_profile', name='other_profile'),
    url(r'^edit$', 'ProfileEdit', name='profile_edit')
)
