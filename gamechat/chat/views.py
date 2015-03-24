from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from chat.models import ChatRoom
import time


def index(request):
    chat_rooms = ChatRoom.objects.order_by('name')[:5]
    context = {
        'chat_list': chat_rooms,
    }
    return render(request, 'chats/index.html', context)


def chat_room(request, chat_room_id):
    chatid = get_object_or_404(ChatRoom, pk=chat_room_id)
    context = {
        'chatroom': chatid,
    }
    return render(request, 'chats/chat_room.html', context)


@csrf_exempt
def chat_add(request, chat_room_id):
    # print "this is a test"
    # import pdb; pdb.set_trace()
    message = request.POST.get('message')
    chat_room = ChatRoom.objects.get(pk=chat_room_id)
    chat_room.add(message)
    return JsonResponse({'message': message})


@csrf_exempt
def chat_messages(request, chat_room_id):
    chat_room = ChatRoom.objects.get(pk=chat_room_id)
    data = {
        'messages': chat_room.messages[-1],
    }
    time.sleep(5)
    return JsonResponse(data)
