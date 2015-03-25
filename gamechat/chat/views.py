from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import JsonResponse
from chat.models import ChatRoom
from gevent import queue


QUEUES = {'Chat Room': {'User': queue.Queue(), }, }
ssb = {'Chat Room': {'User': queue.Queue(), }, }
wow = {'Chat Room': {'User': queue.Queue(), }, }
lol = {'Chat Room': {'User': queue.Queue(), }, }
cs = {'Chat Room': {'User': queue.Queue(), }, }
destiny = {'Chat Room': {'User': queue.Queue(), }, }
mine = {'Chat Room': {'User': queue.Queue(), }, }
hearth = {'Chat Room': {'User': queue.Queue(), }, }
dota = {'Chat Room': {'User': queue.Queue(), }, }
diablo = {'Chat Room': {'User': queue.Queue(), }, }
local = {'Chat Room': {'User': queue.Queue(), }, }

dict_of_queus = {'ssb': ssb, 'wow': wow, 'lol': lol, 'cs': cs, 'destiny': destiny,
                 'mine': mine, 'hearth': hearth, 'dota': dota, 'diablo': diablo,
                 'local': local}


chatrooms = ChatRoom.objects.all()
for chatroom in chatrooms:
    if chatroom.main in dict_of_queus:
        dict_of_queus[chatroom.main][chatroom.name] = {}


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
    main = request.path.rsplit('/', 2)[-1]
    name = request.POST.get('Enter a New Room Name')
    new_room = ChatRoom()
    new_room.name = name
    if main in dict_of_queus:
        new_room.main = main
        main = dict_of_queus[main]
    else:
        main = QUEUES
    new_room.owner = request.user.profile
    new_room.save()
    main[name] = {}
    return chat_room(request, new_room.pk)


def chat_room(request, chat_room_id):
    room = ChatRoom.objects.get(pk=chat_room_id)
    sel_queue = dict_of_queus[room.main]
    context = {
        'chatroom': room,
        'subs': room.subscribers.all(),
        'rooms': room.name,
        # 'queues': QUEUES,
    }
    if request.user.profile:
        room.add_subscriber(request.user.profile)
        sel_queue[room.name][request.user.username] = queue.Queue()

    return render(request, 'chat/chat_room.html', context)


@csrf_exempt
def chat_add(request, chat_room_id):
    message = request.POST.get('message')
    chat_room = ChatRoom.objects.get(pk=chat_room_id)
    chat_room_name = chat_room.name
    sel_queue = dict_of_queus[chat_room.main]
    for prof in sel_queue[chat_room_name]:
        msg = "{}:    {}".format(request.user.username, message)
        sel_queue[chat_room_name][prof].put_nowait(msg)

    return JsonResponse({'message': message})


@csrf_exempt
def chat_messages(request, chat_room_id):
    chat_room = ChatRoom.objects.get(pk=chat_room_id)
    chat_room_main = chat_room.main
    chat_room_name = chat_room.name
    sel_queue = dict_of_queus[chat_room_main]
    try:
        q = sel_queue[chat_room_name][request.user.username]
        print request.user.username
        msg = q.get(timeout=1)
    except queue.Empty:
        msg = []

    data = {
        'messages': msg,
    }

    return JsonResponse(data)


def delete_chatroom(request, chat_room_id):
    if request.user.profile == ChatRoom.objects.get(pk=chat_room_id).owner:
        channel = ChatRoom.objects.get(pk=chat_room_id).main
        ChatRoom.objects.get(pk=chat_room_id).delete()
        url = '/chat/' + channel
    return redirect(url)
