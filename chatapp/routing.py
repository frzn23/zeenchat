# chatapp/routing.py
from django.urls import re_path
from . import consumers

urlpatterns = [
     re_path(r'ws/status/$', consumers.ChatConsumer.as_asgi()),
     re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),
]