from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from views import update_picture
import views

urlpatterns = patterns('profiles.views',
    url(r'^$', 'profile', name='profile'),
    url(r'^(?P<slug>[\w\-]+)/$', 'other_profile', name='other_profile'),
    url(r'^profile_list', login_required(views.ListProfiles.as_view(
        template_name="profiles/profile_list.html")),
        name='profile_list'),
    url(r'^friend/(?P<pk>\d+)$', 'make_friends', name='profile_edit'),
    url(r'^block/(?P<pk>\d+)$', 'block_asshole', name='profile_edit'),
    url(r'^request_friend/(?P<pk>\d+)$', 'make_friends', name='request_friend'),
    url(r'^add_friend/(?P<pk>\d+)$', 'add_friend', name='add_friend'),
    url(r'^unfriend/(?P<pk>\d+)$', 'unfriend', name='unfriend'),
    url(r'^block/(?P<pk>\d+)$', 'block_asshole', name='block_asshole'),
    url(r'^unblock/(?P<pk>\d+)$', 'unblock_asshole', name='unblock_asshole'),
    url(r'^picture/(?P<pk>\d+)$', login_required(update_picture.as_view()), name='update_picture'),
    url(r'^accept_invite/(?P<pk>\d+)$', 'accept_invitation', name='accept_invitation'),
    url(r'^deny_invite/(?P<pk>\d+)$', 'deny_invitation', name='deny_invitation'),

)
