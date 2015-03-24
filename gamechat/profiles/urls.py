from django.conf.urls import patterns, url

urlpatterns = patterns('profiles.views',
    url(r'^profile/$', 'profile', name='profile'),
    url(r'^profile/edit$', 'ProfileEdit', name='profile_edit')
)
