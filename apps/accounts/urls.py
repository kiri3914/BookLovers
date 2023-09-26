from django.urls import path
from . import views
from .views import user_list

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
     path('user_list/', user_list, name='user_list'),

]