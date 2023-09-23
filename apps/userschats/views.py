from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.core.paginator import Paginator
from .models import ChatRoom, Message
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
    private_chats = request.user.chatrooms.filter(is_group=False)
    group_chats = request.user.chatrooms.filter(is_group=True)
    return render(request, 'userschats/chat_list.html', {'private_chats': private_chats, 'group_chats': group_chats})



@login_required
def create_private_chat(request, user_id):
    user2 = CustomUser.objects.get(id=user_id)
    chatroom = ChatRoom.objects.create(is_group=False)
    chatroom.participants.add(request.user, user2)
    chatroom.save()
    return redirect('chatroom_detail', chatroom_id=chatroom.id)


@login_required
def create_group_chat(request):
    users2 = CustomUser.objects.exclude(id=request.user.id)
    paginator = Paginator(users2, 10)  # Допустим, 10 пользователей на страницу
    page = request.GET.get('page')
    users_for_page = paginator.get_page(page)
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
    return render(request, 'userschats/create_group_chat.html',
                  {'users': users, 'users2': users_for_page})



@login_required
def send_message(request, chatroom_id):
    chatroom = ChatRoom.objects.get(id=chatroom_id)
    if request.user not in chatroom.participants.all():
        return HttpResponseForbidden("You don't have permission to access this chat.")

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
def edit_group_chat(request, chatroom_id):
    chatroom = get_object_or_404(ChatRoom, id=chatroom_id)
    if request.method == "POST":
        room_name = request.POST.get('room_name')
        user_ids = request.POST.getlist('users')
        chatroom.room_name = room_name
        chatroom.participants.clear()
        for user_id in user_ids:
            user = CustomUser.objects.get(id=user_id)
            chatroom.participants.add(user)
        chatroom.save()
        return redirect('chatroom_detail', chatroom_id=chatroom.id)
    users = CustomUser.objects.exclude(id=request.user.id)
    return render(request, 'userschats/edit_chatroom.html', {'users': users, 'chatroom': chatroom})


@login_required
def delete_chatroom(request, chatroom_id):
    chatroom = get_object_or_404(ChatRoom, id=chatroom_id)
    if request.user not in chatroom.participants.all():
        return HttpResponseForbidden("You don't have permission to delete this chat.")
    if request.method == "POST":
        chatroom.delete()
        return redirect('chat_list')
    return render(request, 'userschats/confirm_delete.html', {'chatroom': chatroom})

@login_required
def private_chat_list(request):
    private_chats = request.user.chatrooms.filter(is_group=False)
    chat_data = []
    for chat in private_chats:
        other_participant = chat.participants.exclude(id=request.user.id).first()
        chat_data.append({'chat': chat, 'other_participant': other_participant})
    return render(request, 'userschats/private_chat_list.html', {'chat_data': chat_data})


@login_required
def create_or_open_private_chat(request, user_id):
    user2 = get_object_or_404(CustomUser, id=user_id)

    if user2 == request.user:
        return HttpResponseForbidden("You cannot create a chat with yourself.")

    chatroom = ChatRoom.objects.filter(
        Q(participants=request.user) & Q(participants=user2) & Q(is_group=False)
    ).first()

    if not chatroom:
        chatroom = ChatRoom.objects.create(is_group=False)
        chatroom.participants.add(request.user, user2)

    return redirect('private_chat_detail', chatroom_id=chatroom.id)


@login_required
def private_chat_detail(request, chatroom_id):
    chatroom = get_object_or_404(ChatRoom, id=chatroom_id, is_group=False)
    other_participant = chatroom.get_other_participant(request.user)
    messages = chatroom.messages.all().order_by('timestamp')

    if request.method == "POST":
        content = request.POST.get('content')
        Message.objects.create(chatroom=chatroom, sender=request.user, content=content)
        return redirect('private_chat_detail', chatroom_id=chatroom.id)

    return render(request, 'userschats/private_chat_detail.html',
                  {'chatroom': chatroom, 'other_participant': other_participant, 'messages': messages})


