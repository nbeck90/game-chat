from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.contrib import admin
from gamechat import settings
from django.conf import settings as dcs
from django.conf.urls.static import static
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/chat/')),
    url(r'^chat/', include('chat.urls')),
    url(r'^profile/', include('profiles.urls'), name='profile'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^calendar/', include('game_calendar.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/profile', RedirectView.as_view(url='/profile/')),
)
if settings.DEBUG:
    urlpatterns += static(dcs.MEDIA_URL, document_root=dcs.MEDIA_ROOT)