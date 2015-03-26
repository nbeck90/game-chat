from django.apps import apps
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from chat.models import ChatRoom
from gevent import queue


chat_app = apps.get_app_config('chat')


QUEUES = chat_app.QUEUES


list_of_queus = ['ssb', 'wow', 'lol', 'cs', 'destiny',
                 'mine', 'hearth', 'dota', 'diablo',
                 'local']


def check_queues():
    chatrooms = ChatRoom.objects.all()
    for chatroom in chatrooms:
        if chatroom.main in list_of_queus:
            QUEUES[chatroom.name] = {}

chatrooms = ChatRoom.objects.all()
for chatroom in chatrooms:
    QUEUES[chatroom.name] = {}


@csrf_exempt
def index(request):
    name = request.path.rsplit('/', 1)[1]
    chat_room = []
    for room in ChatRoom.objects.filter(main=name).all():
        users = len(room.subscribers.all())
        chat_room.append((room, users))
    context = {
        'chat_list': chat_room,
        'channel': name,
    }
    print QUEUES
    return render(request, 'chat/index.html', context)


@csrf_exempt
def create_room(request):
    request.user.profile.own_room = True
    request.user.profile.save()
    main = request.path.rsplit('/', 2)[-1]
    name = request.POST.get('Enter a New Room Name')
    new_room = ChatRoom()
    new_room.name = name
    new_room.owner = request.user.profile
    new_room.main = main
    new_room.save()
    QUEUES[name] = {}
    print QUEUES
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
    print QUEUES
    return render(request, 'chat/chat_room.html', context)


@csrf_exempt
def chat_add(request, chat_room_id):
    print "-"*50
    print "in 'add': {}".format(QUEUES)
    print "this is the QUEUES object id: {}".format(id(QUEUES))
    print "-"*50
    message = request.POST.get('message')
    chat_room = ChatRoom.objects.get(pk=chat_room_id).name
    for prof in QUEUES[chat_room]:
        msg = "{}:    {}".format(request.user.username, message)
        QUEUES[chat_room][prof].put_nowait(msg)
    return JsonResponse({'message': message})


@csrf_exempt
def chat_messages(request, chat_room_id):
    print "*"*50
    print "in get: {}".format(QUEUES)
    print "this is the QUEUES object id: {}".format(id(QUEUES))
    print "*"*50
    chat_room = ChatRoom.objects.get(pk=chat_room_id).name
    try:
        q = QUEUES[chat_room][request.user.username]
        msg = q.get(timeout=1)
        name = msg.split()[0][:-1]
        if request.user.profile.blocking.filter(user__username=name):
            msg = ["{}:    {}".format(name, 'blocked')]
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
