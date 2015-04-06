from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django.http import JsonResponse
from django.db import IntegrityError
from chat.models import ChatRoom, Message
from profiles.models import Profile
from gamechat.urls import QUEUES
from gevent import queue


list_of_games = ['ssb', 'wow', 'lol', 'cs', 'destiny',
                 'mine', 'hearth', 'dota', 'diablo',
                 'local']


chatrooms = ChatRoom.objects.all()
for chatroom in chatrooms:
    QUEUES[chatroom.name] = {}


@csrf_exempt
@login_required
def index(request, name):
    """
    After picking a game this page will show all the chat rooms available
    """
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
        return redirect(reverse('four'))


@csrf_exempt
@login_required
def create_room(request, main):
    """
    Create a chat room for a game after going to the index page
    """
    request.user.profile.save()
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


@login_required
def chat_room(request, chat_room_id):
    """
    After picking a chat room add the user to the subscriber and

    add the chatroom too profile
    """
    try:
        chatroom = ChatRoom.objects.get(pk=chat_room_id)
        user = Profile.objects.get(user=request.user)
        user.chat_room_name = chatroom.name
        user.save()
        active = Profile.objects.filter(chat_room_name=chatroom.name)
        context = {
            'chatroom': chatroom,
            'subs': active,
            'rooms': chatroom.name,
        }
        if request.user.profile:
            chatroom.add_subscriber(request.user.profile)
            QUEUES[chatroom.name][request.user.username] = queue.Queue()
        return render(request, 'chat/chat_room.html', context)
    except ChatRoom.DoesNotExist:
        return redirect(reverse('four'))


@csrf_exempt
def chat_add(request, chat_room_id):
    """
    Contributing to chat, formatted to have the username.

    Accept unicode in the chat
    """
    message = request.POST.get('message')
    room = ChatRoom.objects.get(pk=chat_room_id)
    profile = Profile.objects.get(user=request.user)

    Message.objects.create(
            profile=profile,
            text=message,
            room=room,
            )

    if message:
        chat_room = ChatRoom.objects.get(pk=chat_room_id).name
        for prof in QUEUES[chat_room]:
            message = unicode(message)
            message = message.encode('utf-8')
            msg = "{}: {}".format(request.user.username, message)
            QUEUES[chat_room][prof].put_nowait(msg)

    return JsonResponse({'message': message})


@csrf_exempt
def chat_messages(request, chat_room_id):
    """
    Receiving messages for a user
    """
    chat_room = ChatRoom.objects.get(pk=chat_room_id).name
    try:
        q = QUEUES[chat_room][request.user.username]
        msg = q.get(timeout=.05)
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
    """
    Owner deletes the chatroom he has created
    """
    request.user.profile.own_room = False
    request.user.profile.save()
    if request.user.profile == ChatRoom.objects.get(pk=chat_room_id).owner:
        ChatRoom.objects.get(pk=chat_room_id).delete()
        request.user.profile.Created_room = False
    return redirect('/')
