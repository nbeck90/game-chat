from django.conf.urls import patterns, include, url
from django.contrib import admin
from gamechat import settings
from django.conf import settings as dcs
from django.conf.urls.static import static
from django.views.generic import RedirectView
from chat_container import QueueContainer


QUEUES = QueueContainer()


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'gamechat.views.home_page', name='home'),
    url(r'^chat/', include('chat.urls'), name='chat'),
    url(r'^profile/', include('profiles.urls'), name='profile'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^calendar/', include('game_calendar.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/profile', RedirectView.as_view(url='/profile/')),
)
if settings.DEBUG:
    urlpatterns += static(dcs.MEDIA_URL, document_root=dcs.MEDIA_ROOT)
