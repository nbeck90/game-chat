from django.conf.urls import patterns, url
from profiles.views import ProfileEdit, Profile, ProfileOther
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('profiles.views',
    url(r'^profile/$', login_required(Profile).as_view(), name='profile'),
    url(r'^profile/edit/$', login_required(ProfileEdit.as_view()), name='profile_edit'),
    url(r'^profile/(?P<pk>\d+)/$', login_required(ProfileOther).as_view, name='profile_other')
)
