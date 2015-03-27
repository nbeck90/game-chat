from django.conf.urls import patterns, url
import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',

                       url(r'^$',
                           views.calendar,
                           name='calendar_view'),
                       url(r'^event_detail/(?P<pk>\d+)$',
                           views.event_detail,
                           name='event_detail'),
                       url(r'^event_feed/$',
                           views.return_event,
                           name='event_feed'),
                       url(r'^create_event/$', login_required(views.EventCreate.as_view(
                           template_name="game_calendar/create_form.html",
                           success_url='/calendar/')),
                           name='create_form'),
                       url(r'^delete_event/(?P<pk>\d+)$', login_required(views.EventDelete.as_view(
                           template_name="game_calendar/delete_form.html",
                           success_url='/calendar/')),
                           name='delete_event'),
                       )
