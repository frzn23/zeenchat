from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.users, name='users'),
    path('chat/<str:username>/', views.chat, name='chat'),
    path('save-message/', views.save_message, name='save_message'),
    path('get-unread-counts/', views.get_unread_counts, name='get_unread_counts'),
    path('add-friend/', views.add_friend, name='send_friend_request'),
    path('friend-request/<str:action>/', views.accept_or_decline_request, name='send_friend_request'),
]