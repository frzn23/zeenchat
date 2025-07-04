from django.contrib import admin
from .models import Message, FriendRequest
# Register your models here.
admin.site.register(Message)
admin.site.register(FriendRequest)