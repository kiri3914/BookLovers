from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .models import UserProfile, Friend
from ..accounts.models import CustomUser

from django.db.models import Q


@login_required
def my_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    context = {
        'user_profile': user_profile
    }
    return render(request, 'profile/my_profile.html', context)


@login_required
def profile_detail(request, profile_id):
    user_profile = get_object_or_404(UserProfile, id=profile_id)
    if user_profile == request.user.user_profile:
        return redirect ('my_profile')
    # Получить список друзей пользователя
    friends = Friend.objects.filter(user=user_profile.user, status='accepted')
    
    context = {'user_profile': user_profile, 'friends': friends}
    return render(request, 'profile/profile_detail.html', context)

def send_friend_request(request, user_id):
    user = request.user
    friend = get_object_or_404(CustomUser, id=user_id)
    is_friend = Friend.objects.filter(Q(user=user, friend=friend)|Q(user=friend,friend=user),status='accepted').exists()
    if is_friend:
        messages.error(request,'Вы уже в списке друзей')
    else:
        Friend.objects.get_or_create(friend=friend, user=user)
    return redirect('profile_detail', profile_id=friend.user_profile.id)


@login_required
def friends_list(request):
    friends_requests = Friend.objects.filter(friend=request.user,
                                             status='pending')
    context = {
        'friends_requests': friends_requests
    }
    return render(request, 'profile/friends_list.html', context=context)


@login_required
def accept_friend_request(request, user_id):
    friend_request = get_object_or_404(Friend,
                                       friend=request.user,
                                       user__id=user_id,
                                       status='pending')
    friend_request.status = 'accepted'
    friend_request.save()
    return redirect('friends_list')


@login_required
def rejected_friend_request(request, user_id):
    friend_request = get_object_or_404(Friend,
                                       friend=request.user,
                                       user__id=user_id,
                                       status='pending')
    friend_request.status = 'rejected'
    friend_request.save()
    return redirect('friends_list')
