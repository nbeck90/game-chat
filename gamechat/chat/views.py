from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from chat.models import ChatRoom


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


def chat_add(request, chat_room_id):
    message = request['message']
    chat_room = ChatRoom.objects.filter(pk=chat_room_id)
    chat_room.add(message)


def chat_messages(request, chat_room_id):
    chat_room = ChatRoom.objects.filter(pk=chat_room_id)
    return JsonResponse({'messages': chat_room.backlog()})
