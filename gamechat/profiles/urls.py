from django.conf.urls import patterns, url
import views

urlpatterns = patterns('profiles.views',
    url(r'^$', 'profile', name='profile'),
    url(r'^(?P<slug>[\w\-]+)/$', 'other_profile', name='other_profile'),
    url(r'^edit$', 'ProfileEdit', name='profile_edit'),
    url(r'^profile_list', (views.ListProfiles.as_view(
        template_name="profiles/profile_list.html")),
        name='profile_list'),
    url(r'^friend/(?P<pk>\d+)$', 'make_friends', name='profile_edit'),
    url(r'^block/(?P<pk>\d+)$', 'block_asshole', name='profile_edit'),
    url(r'^request_friend/(?P<pk>\d+)$', 'make_friends', name='request_friend'),
    url(r'^add_friend/(?P<pk>\d+)$', 'add_friend', name='add_friend'),
    url(r'^block/(?P<pk>\d+)$', 'block_asshole', name='block_asshole'),
    url(r'^unblock/(?P<pk>\d+)$', 'unblock_asshole', name='unblock_asshole'),
)
