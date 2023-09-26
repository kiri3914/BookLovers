from django import template
from django.db.models import Q

from apps.profiles.models import Friend

register = template.Library()


@register.filter(name='has_friend_requests')
def has_friend_requests(user):
    return Friend.objects.filter(friend=user, status='pending').count()
