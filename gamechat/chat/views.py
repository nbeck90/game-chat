from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from chat.models import ChatRoom
from gevent import queue


QUEUES = {'generic': queue.Queue(), }


def index(request):
    chat_rooms = ChatRoom.objects.order_by('name')[:5]
    context = {
        'chat_list': chat_rooms,
    }
    return render(request, 'chat/index.html', context)


def chat_room(request, chat_room_id):
    chatid = get_object_or_404(ChatRoom, pk=chat_room_id)
    room = ChatRoom.objects.get(pk=chat_room_id)
    context = {
        'chatroom': chatid,
        'subs': room.subscribers.all()
    }
    print room.subscribers.all()
    if request.user.profile:
        room.add_subscriber(request.user.profile)
        QUEUES[request.user.username] = queue.Queue()

    return render(request, 'chats/chat_room.html', context)


@csrf_exempt
def chat_add(request, chat_room_id):
    # print "this is a test"
    # import pdb; pdb.set_trace()
    message = request.POST.get('message')
    chat_room = ChatRoom.objects.get(pk=chat_room_id)
    for prof in QUEUES:
        msg = "{}:    {}".format(request.user.username, message)
        QUEUES[prof].put_nowait(msg)

    return JsonResponse({'message': message})


@csrf_exempt
def chat_messages(request, chat_room_id):
    # chat_room = ChatRoom.objects.get(pk=chat_room_id)
    try:
        q = QUEUES[request.user.username]
        print request.user.username
        msg = q.get(timeout=10)
    except queue.Empty:
        msg = []

    data = {
        'messages': msg,
    }

    return JsonResponse(data)
