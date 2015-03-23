from django.conf.urls import patterns, url
import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', views.calendar, name='calendar'),
    )
