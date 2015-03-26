from django.conf.urls import patterns, url
from chat_container import QueueContainer


QUEUES = QueueContainer()


urlpatterns = patterns(
    'chat.views',
    url(r'^\w+$', 'index', name='index'),
    url(r'^room/(?P<chat_room_id>\d+)/$', 'chat_room',
        name='chat_room'),
    url(r'^add/(?P<chat_room_id>\d+)/$', 'chat_add',
        name='chat_add'),
    url(r'^show/(?P<chat_room_id>\d+)/$', 'chat_messages',
        name='chat_messages'),
    url(r'^create/room/\w+$', 'create_room',
        name='create_room'),
    url(r'^delete_room/(?P<chat_room_id>\d+)', 'delete_chatroom',
        name='delete_room')
)
