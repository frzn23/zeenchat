# chatapp/routing.py
from django.urls import re_path
from . import consumers

urlpatterns = [
    re_path(r'ws/chat/(?P<user1>[\w.@+-]+)/(?P<user2>[\w.@+-]+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<user1>[\w.@+-]+)/status/$', consumers.ChatConsumer.as_asgi()),
    # re_path(r'ws/chat/(?P<room_name>[\w.@+-]+)/$', consumers.ChatConsumer.as_asgi()),
]