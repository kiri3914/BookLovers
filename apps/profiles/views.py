from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import UserProfile


@login_required
def my_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    context = {
        'user_profile': user_profile
    }
    return render(request, 'profile/my_profile.html', context)


def profile_detail(request, profile_id):
    user_profile = get_object_or_404(UserProfile, id=profile_id)
    context = {'user_profile': user_profile}
    return render(request, 'profile/profile_detail.html', context)
