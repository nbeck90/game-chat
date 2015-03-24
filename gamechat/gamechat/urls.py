from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',

    url(r'^$', 'gamechat.views.home_page', name='home'),
    url(r'^chat/', include('chat.urls')),
    url(r'^', include('profiles.urls'), name='profile'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^calendar/', include('game_calendar.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
)
