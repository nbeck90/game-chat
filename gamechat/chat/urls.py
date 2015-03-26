from django.conf.urls import patterns, url
from chat_container import QueueContainer


# <<<<<<< HEAD
# urlpatterns = patterns('',
#                url(r'^(?P<name>\w+)$', views.index, name='index'),
#                url(r'^room/(?P<chat_room_id>\d+)/$', views.chat_room,
#                    name='chat_room'),
#                url(r'^add/(?P<chat_room_id>\d+)/$', views.chat_add,
#                    name='chat_add'),
#                url(r'^show/(?P<chat_room_id>\d+)/$', views.chat_messages,
#                    name='chat_messages'),
#                url(r'^create/room/(?P<main>\w+)$', views.create_room,
#                    name='create_room'),
#                url(r'^delete_room/(?P<chat_room_id>\d+)', views.delete_chatroom,
#                    name='delete_room')
# =======
QUEUES = QueueContainer()


urlpatterns = patterns(
    'chat.views',
    url(r'^(?P<name>\w+)$', 'index', name='index'),
    url(r'^room/(?P<chat_room_id>\d+)/$', 'chat_room',
        name='chat_room'),
    url(r'^add/(?P<chat_room_id>\d+)/$', 'chat_add',
        name='chat_add'),
    url(r'^show/(?P<chat_room_id>\d+)/$', 'chat_messages',
        name='chat_messages'),
    url(r'^create/room/(?P<main>\w+)$', 'create_room',
        name='create_room'),
    url(r'^delete_room/(?P<chat_room_id>\d+)', 'delete_chatroom',
        name='delete_room')

)
