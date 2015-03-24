from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from chat.models import ChatRoom
from gevent import queue


QUEUES = {'Test Chat Room 1': {'generic': queue.Queue(), }, }


def index(request):
    chat_rooms = ChatRoom.objects.order_by('name')[:5]
    context = {
        'chat_list': chat_rooms,
    }
    return render(request, 'chats/index.html', context)


@csrf_exempt
def create_room(request):
    name = request.POST.get('Enter a New Room Name')
    new_room = ChatRoom()
    new_room.name = name
    new_room.save()
    QUEUES[name] = {}
    return chat_room(request, new_room.pk)


def chat_room(request, chat_room_id):
    chatroom = get_object_or_404(ChatRoom, pk=chat_room_id)
    room = ChatRoom.objects.get(pk=chat_room_id)
    context = {
        'chatroom': chatroom,
        'subs': room.subscribers.all(),
        'rooms': room.name,
        'queues': QUEUES,
    }
    if request.user.profile:
        room.add_subscriber(request.user.profile)
        QUEUES[chatroom.name][request.user.username] = queue.Queue()

    return render(request, 'chats/chat_room.html', context)


@csrf_exempt
def chat_add(request, chat_room_id):
    message = request.POST.get('message')
    chat_room = ChatRoom.objects.get(pk=chat_room_id).name
    for prof in QUEUES[chat_room]:
        msg = "{}:    {}".format(request.user.username, message)
        QUEUES[chat_room][prof].put_nowait(msg)

    return JsonResponse({'message': message})


@csrf_exempt
def chat_messages(request, chat_room_id):
    chat_room = ChatRoom.objects.get(pk=chat_room_id).name
    try:
        q = QUEUES[chat_room][request.user.username]
        print request.user.username
        msg = q.get(timeout=10)
    except queue.Empty:
        msg = []

    data = {
        'messages': msg,
    }

    return JsonResponse(data)
