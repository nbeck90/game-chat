from django.conf.urls import patterns, url
import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{4})/$',
        views.day_detail,
        name="day_detail"),
    url(r'^(?P<month>\d{2})/(?P<year>\d{4})/$', views.calendar, name='calendar_view'),
    url(r'^event_detail/(?P<pk>\d+)/$', views.event_detail, name='event_detail')
)
