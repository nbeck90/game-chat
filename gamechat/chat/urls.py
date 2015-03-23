from django.conf.urls import patterns, url
from chat import views


urlpatterns = patterns('',
               url(r'^$', views.index, name='index'),
               url(r'^(?P<chat_room_id>\d+)/$', views.chat_room,
                   name='chat_room'),
               url(r'^$add/(?P<chat_room_id>\d+)/$', views.chat_add,
                   name='chat_room'),
               url(r'^$show/(?P<chat_room_id>\d+)/$', views.chat_messages,
                   name='chat_room'),
)
