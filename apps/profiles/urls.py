from django.urls import path
from . import views


urlpatterns = [
    path('', views.my_profile, name='my_profile'),
    path('<int:profile_id>', views.profile_detail, name='profile_detail'),
]