from django.urls import path
from .views import (
    chat_list,
    create_private_chat,
    create_group_chat,
    send_message,
    chatroom_detail,
    edit_group_chat,
    delete_chatroom,
    get_users,
    create_or_open_private_chat,
    private_chat_detail,
    private_chat_list,
    search_users,
)

urlpatterns = [
    path('chats/', chat_list, name='chat_list'),
    path('get-users/', get_users, name='get_users'),
    path('create-private-chat/<int:user_id>/', create_private_chat, name='create_private_chat'),
    path('create-group-chat/', create_group_chat, name='create_group_chat'),
    path('send-message/<int:chatroom_id>/', send_message, name='send_message'),
    path('chatroom/<int:chatroom_id>/', chatroom_detail, name='chatroom_detail'),
    path('edit-chatroom/<int:chatroom_id>/', edit_group_chat, name='edit_chatroom'),
    path('delete-chatroom/<int:chatroom_id>/', delete_chatroom, name='delete_chatroom'),
    path('create-or-open-private-chat/<int:user_id>/', create_or_open_private_chat, name='create_or_open_private_chat'),
    path('private-chatroom-detail/<int:chatroom_id>/', private_chat_detail, name='private_chat_detail'),
    path('private-chats/', private_chat_list, name='private_chat_list'),
    path('search_users/', search_users, name='search_users'),
]
