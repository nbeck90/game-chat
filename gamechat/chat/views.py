from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import IntegrityError
from chat.models import ChatRoom
from gevent import queue


QUEUES = {
          'Chat Room': {'User': queue.Queue(), },
          }


list_of_queus = ['ssb', 'wow', 'lol', 'cs', 'destiny',
                 'mine', 'hearth', 'dota', 'diablo',
                 'local']


def check_queues():
    chatrooms = ChatRoom.objects.all()
    for chatroom in chatrooms:
        if chatroom.main in list_of_queus:
            QUEUES[chatroom.name] = {}


@csrf_exempt
def index(request):
    name = request.path.rsplit('/', 1)[1]
    chat_room = []
    for room in ChatRoom.objects.filter(main=name).all():
        chat_room.append(room)
    context = {
        'chat_list': chat_room,
        'channel': name,
    }
    return render(request, 'chat/index.html', context)


@csrf_exempt
def create_room(request):
    try:
        main = request.path.rsplit('/', 2)[-1]
        name = request.POST.get('Enter a New Room Name')
        new_room = ChatRoom()
        new_room.name = name
        if main in list_of_queus:
            new_room.main = main
        new_room.owner = request.user.profile
        new_room.save()
        QUEUES[name] = {}
        check_queues()
        return chat_room(request, new_room.pk)
    except IntegrityError:
        return redirect('/')


@csrf_exempt
def chat_room(request, chat_room_id):
    room = ChatRoom.objects.get(pk=chat_room_id)
    room_name = str(room.name)
    user = request.user.username
    context = {
        'chatroom': room,
        'subs': room.subscribers.all(),
        'rooms': room.name,
        'queues': QUEUES,
    }
    # print "test"
    # print request.user.profile
    if request.user.profile:
        room.add_subscriber(request.user.profile)
        check_queues()
        QUEUES[room_name].update({user: queue.Queue()})

    return render(request, 'chat/chat_room.html', context)


@csrf_exempt
def chat_add(request, chat_room_id):
    message = request.POST.get('message')
    chat_room = ChatRoom.objects.get(pk=chat_room_id)
    chat_room_name = chat_room.name
    user = request.user.username
    for prof in QUEUES[chat_room_name]:
        msg = "{}:    {}".format(user, message)
        QUEUES.get(chat_room_name).get(user).put_nowait(msg)

    return JsonResponse({'message': message})


@csrf_exempt
def chat_messages(request, chat_room_id):
    chat_room = ChatRoom.objects.get(pk=chat_room_id)
    chat_room_name = chat_room.name
    user = request.user.username
    # print request.user.username
    # print QUEUES[chat_room_name][user]
    # check_queues()
    # print QUEUES
    try:
        msg = QUEUES.get(chat_room_name).get(user).get(timeout=10)
    except queue.Empty:
        msg = []

    data = {
        'messages': msg,
    }

    return JsonResponse(data)


@csrf_exempt
def delete_chatroom(request, chat_room_id):
    if request.user.profile == ChatRoom.objects.get(pk=chat_room_id).owner:
        channel = ChatRoom.objects.get(pk=chat_room_id).main
        ChatRoom.objects.get(pk=chat_room_id).delete()
        url = '/chat/' + channel
    return redirect(url)
