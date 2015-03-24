from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gamechat.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^(/)?$', RedirectView.as_view(url='/chat/')),
    url(r'^chat/', include('chat.urls')),
    url(r'^', include('profiles.urls'), name='profile'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^calendar/', include('game_calendar.urls')),
)
