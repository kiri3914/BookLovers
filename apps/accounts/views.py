from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from .forms import CustomUserCreationForm,UserSearchForm

from django.contrib.auth.decorators import login_required
from .models import CustomUser

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('my_profile')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})



@login_required
def user_list(request):
    users = CustomUser.objects.exclude(id=request.user.id)  
    context = {
        'users': users,
    }
    return render(request, 'accounts/user_list.html', context)




@login_required
def user_list(request):
    users = CustomUser.objects.all()
    form = UserSearchForm(request.GET)
    
    if form.is_valid():
        search_query = form.cleaned_data['search_query']
        users = users.filter(username__icontains=search_query)
    
    context = {'users': users, 'form': form}
    return render(request, 'accounts/user_list.html', context)
