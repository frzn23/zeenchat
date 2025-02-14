from django.shortcuts import render
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from .views import CustomLoginView

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.users, name='users'),
    path('chat/<str:username>/', views.chat, name='chat'),
    path('save-message/', views.save_message, name='save_message'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),  # Replace default login view
]