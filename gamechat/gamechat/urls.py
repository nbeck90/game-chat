from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/chat/')),
    url(r'^chat/', include('chat.urls')),
    url(r'^profile/', include('profiles.urls'), name='profile'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^calendar/', include('game_calendar.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
)
