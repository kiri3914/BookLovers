from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, redirect
from .models import Friend
from ..accounts.models import CustomUser

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile


@login_required
def view_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    friends = Friend.objects.filter(friend=user_profile.user, status='accepted')
    context = {
        'user_profile': user_profile,
        'friends': friends
    }
    return render(request, 'profile/my_profile.html', context)


def profile_detail(request, profile_id):
    user_profile = get_object_or_404(UserProfile, id=profile_id)
    context = {
        'user_profile': user_profile
    }
    return render(request, 'profile/view_profile.html', context)


def sent_friend_request(request, friend_id):
    user = request.user
    friend = get_object_or_404(CustomUser, id=friend_id)
    Friend.objects.get_or_create(user=user, friend=friend)
    return redirect('profile_detail', profile_id=friend.user_profile.id)


def accept_friend_request(request, friend_id):
    friend_request = get_object_or_404(Friend, id=friend_id, friend=request.user, status='pending')
    friend_request.status = 'accepted'
    friend_request.save()

    return redirect('profile_detail', profile_id=request.user.user_profile.id)
