from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_profile, name='profile'),
    path('<int:profile_id>', views.profile_detail, name='profile_detail'),

    # URL-маршрут для отправки запроса на добавление в друзья
    path('add_friend/<int:friend_id>/', views.sent_friend_request, name='sent_friend_request'),

    # URL-маршрут для принятия запроса на добавление в друзья
    path('accept_friend_request/<int:friend_id>/', views.accept_friend_request, name='accept_friend_request'),
]
