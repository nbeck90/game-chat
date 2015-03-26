from django.conf.urls import patterns, url
import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',

                       url(r'^(?P<month>\d{2})/(?P<year>\d{4})/$',
                           views.calendar,
                           name='calendar_view'),
                       url(r'^event_feed/$',
                           views.return_event,
                           name='event_feed')
                       )
