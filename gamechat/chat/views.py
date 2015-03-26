from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.html import escape
from django.http import JsonResponse
from django.db import IntegrityError
from chat.models import ChatRoom
from profiles.models import Profile
from gamechat.urls import QUEUES
from gevent import queue


list_of_games = ['ssb', 'wow', 'lol', 'cs', 'destiny',
                 'mine', 'hearth', 'dota', 'diablo',
                 'local']

# def check_queues():
#     chatrooms = ChatRoom.objects.all()
#     for chatroom in chatrooms:
#         if chatroom.main in list_of_games:
#             QUEUES[chatroom.name] = {}

chatrooms = ChatRoom.objects.all()
for chatroom in chatrooms:
    QUEUES[chatroom.name] = {}


@csrf_exempt
def index(request, name):
    # name = request.path.rsplit('/', 1)[1]
    if name in list_of_games:
        chat_room = []
        for room in ChatRoom.objects.filter(main=name).all():
            users = len(Profile.objects.filter(chat_room_name=room.name))
            chat_room.append((room, users))
        context = {
            'chat_list': chat_room,
            'channel': name,
        }
        return render(request, 'chat/index.html', context)
    else:
        return redirect('/')


@csrf_exempt
def create_room(request, main):
    request.user.profile.own_room = True
    request.user.profile.save()
    # main = request.path.rsplit('/', 2)[-1]
    name = request.POST.get('Enter a New Room Name')
    try:
        if name.strip():
            request.user.profile.own_room = True
            request.user.profile.save()
            new_room = ChatRoom()
            new_room.name = name
            new_room.owner = request.user.profile
            new_room.main = main
            new_room.save()
            QUEUES[name] = {}
            return redirect('/chat/room/' + str(new_room.pk))
    except IntegrityError, AttributeError:
        pass
    return redirect('/chat/' + main)


def chat_room(request, chat_room_id):
    chatroom = get_object_or_404(ChatRoom, pk=chat_room_id)
    # room = ChatRoom.objects.get(pk=chat_room_id)
    user = Profile.objects.get(user=request.user)
    user.chat_room_name = chatroom.name
    user.save()
    active = Profile.objects.filter(chat_room_name=chatroom.name)
    context = {
        'chatroom': chatroom,
        'subs': active,
        'rooms': chatroom.name,
        # 'queues': QUEUES,
    }
    if request.user.profile:
        chatroom.add_subscriber(request.user.profile)
        QUEUES[chatroom.name][request.user.username] = queue.Queue()
    return render(request, 'chat/chat_room.html', context)


@csrf_exempt
def chat_add(request, chat_room_id):
    message = request.POST.get('message')
    if message:
        chat_room = ChatRoom.objects.get(pk=chat_room_id).name
        for prof in QUEUES[chat_room]:
            msg = "{}: {}".format(request.user.username, message)
            QUEUES[chat_room][prof].put_nowait(msg)

    return JsonResponse({'message': message})


@csrf_exempt
def chat_messages(request, chat_room_id):
    chat_room = ChatRoom.objects.get(pk=chat_room_id).name
    try:
        q = QUEUES[chat_room][request.user.username]
        msg = q.get(timeout=.5)
        msg = escape(msg)
        name = msg.split()[0][:-1]
        if request.user.profile.blocking.filter(user__username=name):
            msg = ["{}: {}".format(name, 'blocked')]
    except queue.Empty:
        msg = []

    data = {
        'messages': msg,
    }

    return JsonResponse(data)


def delete_chatroom(request, chat_room_id):
    request.user.profile.own_room = False
    request.user.profile.save()
    if request.user.profile == ChatRoom.objects.get(pk=chat_room_id).owner:
        ChatRoom.objects.get(pk=chat_room_id).delete()
        request.user.profile.Created_room = False
    return redirect('/')
