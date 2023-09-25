from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .forms import UserForm
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
        return redirect('my_profile')
    # Получить список друзей пользователя
    friends = Friend.objects.filter(user=user_profile.user, status='accepted')

    user = request.user
    friend = user_profile.user
    is_friend = Friend.objects.filter(Q(user=user, friend=friend) | Q(user=friend, friend=user)).first()

    context = {'user_profile': user_profile, 'friends': friends, 'is_friend': is_friend}
    return render(request, 'profile/profile_detail.html', context)


@login_required
def edit_profile(request):
    user = request.user  # Получаем текущего пользователя

    if request.method == 'POST':
        print(request.FILES)
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.phone_number = form.cleaned_data['phone_number']
            user.birthdate = form.cleaned_data['birthdate']
            user.bio = form.cleaned_data['bio']
            if 'profile_picture' in request.FILES:
                user.user_profile.profile_picture = request.FILES['profile_picture']
            user.save()
            user.user_profile.save()

            # Обновляем любимые жанры
            user.user_profile.favorite_genres.set(form.cleaned_data['favorite_genres'])

            return redirect('my_profile')
    else:
        initial_data = {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': user.phone_number,
            'birthdate': user.birthdate,
            'bio': user.bio,
            'favorite_genres': user.user_profile.favorite_genres.all(),
            'profile_picture': user.user_profile.profile_picture,
        }
        form = UserForm(initial=initial_data)

    context = {
        'form': form
    }

    return render(request, 'profile/edit_profile.html', context)


@login_required
def send_friend_request(request, user_id):
    user = request.user
    friend = get_object_or_404(CustomUser, id=user_id)
    is_friend = Friend.objects.filter(Q(user=user, friend=friend) | Q(user=friend, friend=user),
                                      status='accepted').exists()
    if is_friend:
        messages.error(request, 'Вы уже в списке друзей')
    else:
        Friend.objects.get_or_create(friend=friend, user=user)
        messages.success(request, 'Вы успешно отправили запрос на дружбу')
    return redirect('profile_detail', profile_id=friend.user_profile.id)


@login_required
def delete_friend(request, user_id):
    user = request.user
    friend = get_object_or_404(CustomUser, id=user_id)
    obj = Friend.objects.filter(Q(user=user, friend=friend) | Q(user=friend, friend=user)).first()
    if obj:
        obj.delete()
        if obj.status == 'accepted':
            messages.success(request, 'Вы успешно удалили пользователя из списке друзей')
        else:
            messages.success(request, 'Вы успешно отменили запрос на дружбу')
    else:
        messages.error(request, 'Пользователь не найден в списке друзей')
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
