from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from .forms import CustomUserCreationForm


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


from django.shortcuts import render
from django.contrib.gis.geoip2 import GeoIP2

def get_location(request):
    user_ip = get_client_ip(request)
    if user_ip:
        geoip = GeoIP2()
        try:
            location = geoip.city(user_ip)
            city = location.get('city', '')
            country = location.get('country_name', '')
            return render(request, 'location.html', {'city': city, 'country': country})
        except Exception as e:
            error_message = str(e)
            return render(request, 'error.html', {'error_message': error_message})
    else:
        return render(request, 'error.html', {'error_message': 'Unable to determine user IP'})

# Функция для получения IP-адреса пользователя
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
