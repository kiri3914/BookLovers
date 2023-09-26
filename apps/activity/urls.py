from django.urls import path
from . import views

urlpatterns = [
    path('', views.activity_feed, name='activity_feed'),
    path('404/', views.handler404, name='404'),
]
