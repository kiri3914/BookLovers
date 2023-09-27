from django import template
from django.db.models import Q
from apps.userschats.models import Message, ChatRoom
from apps.profiles.models import Friend

register = template.Library()


@register.filter(name='has_friend_requests')
def has_friend_requests(user):
    return Friend.objects.filter(friend=user, status='pending').count()


@register.filter
def unread_messages_count(user):
    return Message.objects.filter(chatroom__participants=user, is_read=False).exclude(sender=user).count()


@register.filter(name='has_unread_messages')
def has_unread_messages(user, another_user):
    return Message.objects.filter(sender=another_user, recipient=user, is_read=False).exists()
