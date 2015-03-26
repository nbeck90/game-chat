from django.conf.urls import patterns, url
import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',

                       url(r'^$',
                           views.calendar,
                           name='calendar_view'),
                       url(r'^event_feed/$',
                           views.return_event,
                           name='event_feed'),
                       url(r'^create_event/$', login_required(views.EventCreate.as_view(
                           template_name="game_calendar/create_form.html",
                           success_url='/profile/')),
                           name='create_form'),
                       )
