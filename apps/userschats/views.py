from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import ChatRoom, Message
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator

from apps.accounts.models import CustomUser


def get_users(request):
    page = int(request.GET.get('page', 1))
    search_query = request.GET.get('search', '')
    users = CustomUser.objects.filter(username__icontains=search_query)
    paginator = Paginator(users, 10)
    current_page_users = paginator.get_page(page)

    users_list = [
        {'id': user.id, 'username': user.username}
        for user in current_page_users
    ]

    return JsonResponse(users_list, safe=False)


@login_required
def chat_list(request):
    chatrooms = request.user.chatrooms.all()
    return render(request, 'userschats/chat_list.html', {'chatrooms': chatrooms})


@login_required
def create_private_chat(request, user_id):
    user2 = CustomUser.objects.get(id=user_id)
    chatroom = ChatRoom.objects.create(is_group=False)
    chatroom.participants.add(request.user, user2)
    chatroom.save()
    return redirect('chatroom_detail', chatroom_id=chatroom.id)


@login_required
def create_group_chat(request):
    if request.method == "POST":
        room_name = request.POST.get('room_name')
        user_ids = request.POST.getlist('users')
        chatroom = ChatRoom.objects.create(is_group=True, room_name=room_name)
        chatroom.participants.add(request.user)
        for user_id in user_ids:
            user = CustomUser.objects.get(id=user_id)
            chatroom.participants.add(user)
        chatroom.save()
        return redirect('chatroom_detail', chatroom_id=chatroom.id)
    users = CustomUser.objects.exclude(id=request.user.id)
    return render(request, 'userschats/create_group_chat.html', {'users': users})


@login_required
def send_message(request, chatroom_id):
    chatroom = ChatRoom.objects.get(id=chatroom_id)
    if request.method == "POST":
        content = request.POST.get('content')
        Message.objects.create(chatroom=chatroom, sender=request.user, content=content)
        return redirect('chatroom_detail', chatroom_id=chatroom.id)
    return render(request, 'userschats/send_message.html', {'chatroom': chatroom})


@login_required
def chatroom_detail(request, chatroom_id):
    chatroom = ChatRoom.objects.get(id=chatroom_id)
    messages = chatroom.messages.all().order_by('timestamp')
    return render(request, 'userschats/chatroom_detail.html', {'chatroom': chatroom, 'messages': messages})


@login_required
def edit_chatroom(request, chatroom_id):
    chatroom = get_object_or_404(ChatRoom, id=chatroom_id)
    if request.method == "POST":
        room_name = request.POST.get('room_name')
        chatroom.room_name = room_name
        chatroom.save()
        return redirect('chatroom_detail', chatroom_id=chatroom.id)
    return render(request, 'userschats/edit_chatroom.html', {'chatroom': chatroom})


@login_required
def delete_chatroom(request, chatroom_id):
    chatroom = get_object_or_404(ChatRoom, id=chatroom_id)
    if request.method == "POST":
        chatroom.delete()
        return redirect('chat_list')
    return render(request, 'userschats/confirm_delete.html', {'chatroom': chatroom})
