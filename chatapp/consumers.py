# chatapp/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import redis
import os
from .redis_manager import update_user_status

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.current_user = self.scope['user'].username
        self.groups = set()  # Track joined groups
        
        # Handle user status
        await self._setup_status_tracking()
        
        # Setup chat room
        await self._setup_chat_room()
        
        await self.accept()

    async def _setup_status_tracking(self):
        """Setup user status tracking."""
        await self.join_group('user_status')
        await self.update_status('online')

    async def _setup_chat_room(self):
        """Setup chat room for two users."""
        user1 = self.scope['url_route']['kwargs']['user1']
        user2 = self.scope['url_route']['kwargs']['user2']
        self.room_name = f"chat_{'_'.join(sorted([user1, user2]))}"
        await self.join_group(self.room_name)

    async def disconnect(self, close_code):
        # Update status and leave all groups
        await self.update_status('offline')
        await self._leave_all_groups()

    async def _leave_all_groups(self):
        """Leave all joined groups."""
        for group in self.groups:
            await self.channel_layer.group_discard(group, self.channel_name)

    async def join_group(self, group_name):
        """Join a channel group and track it."""
        await self.channel_layer.group_add(group_name, self.channel_name)
        self.groups.add(group_name)

    async def update_status(self, status):
        """Update and broadcast user status."""
        update_user_status(self.current_user, status)
        await self.channel_layer.group_send(
            'user_status',
            {
                'type': 'user_status',
                'user': self.current_user,
                'status': status
            }
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    # Add handler for status updates
    async def user_status(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_status',
            'user': event['user'],
            'status': event['status']
        }))