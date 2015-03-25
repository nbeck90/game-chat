from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'gamechat.views.home_page', name='home'),
    url(r'^chat/', include('chat.urls')),
    url(r'^profile/', include('profiles.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^calendar/', include('game_calendar.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/profile', RedirectView.as_view(url='/profile/')),
)
