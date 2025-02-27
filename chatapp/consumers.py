# chatapp/consumers.py
import json
import logging
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from asgiref.sync import async_to_sync

# Set up logging for debugging
logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    """Handles real-time chat and user status updates via WebSocket"""

    async def connect(self):
        """When a user connects to the WebSocket"""
        self.user = self.scope['user']
        if self.user.is_anonymous:
            logger.warning("Anonymous user tried to connect - closing connection")
            await self.close()
            return

        self.lobby_group_name = 'chat_lobby'  # Group for all connected users
        self.private_groups = {}  # Tracks private chat groups for this user

        logger.info(f"{self.user.username} connected with channel {self.channel_name}")

        # Add user to the lobby group for broadcasting status updates
        await self.channel_layer.group_add(self.lobby_group_name, self.channel_name)
        await self.accept()

        # Mark user as online and notify everyone
        await self.update_user_status(True)
        await self.send(text_data=json.dumps({
            'type': 'init',
            'username': self.user.username
        }))
        await self._broadcast_user_list_update()  # Notify all users of the new connection

    async def disconnect(self, close_code):
        """When a user disconnects (e.g., closes tab or logs out)"""
        if not hasattr(self, 'user') or self.user.is_anonymous:
            return

        logger.info(f"{self.user.username} disconnected with code {close_code}")
        
        # Mark user as offline and notify everyone
        await self.update_user_status(False)
        await self.channel_layer.group_discard(self.lobby_group_name, self.channel_name)
        
        # Leave any private chats
        for group_name in self.private_groups.values():
            await self.channel_layer.group_discard(group_name, self.channel_name)
        
        await self._broadcast_user_list_update()  # Let everyone know this user is gone

    async def receive(self, text_data):
        """Handle messages sent from the client"""
        data = json.loads(text_data)
        message_type = data.get('type', 'chat_message')
        logger.debug(f"{self.user.username} sent: {data}")

        handlers = {
            'chat_message': self.handle_chat_message,
            'typing': self.handle_typing,
            'start_chat': self.handle_start_chat
        }
        
        if message_type in handlers:
            await handlers[message_type](data)

    async def handle_start_chat(self, data):
        """Start a private chat with another user"""
        receiver_username = data['receiver']
        group_name = self._generate_group_name(receiver_username)
        self.private_groups[receiver_username] = group_name
        
        await self.channel_layer.group_add(group_name, self.channel_name)
        logger.info(f"{self.user.username} started a chat with {receiver_username} in {group_name}")

    async def handle_chat_message(self, data):
        """Send a message to a private chat group"""
        from django.contrib.auth.models import User
        
        message = data.get('message')
        sender = data.get('sender', self.user.username)
        receiver_username = data.get('receiver')

        if not receiver_username or receiver_username not in self.private_groups:
            logger.warning(f"No chat group found for {receiver_username}")
            return

        try:
            receiver = await database_sync_to_async(User.objects.get)(username=receiver_username)
            message_obj = await self.save_message(message, receiver)
            group_name = self.private_groups[receiver_username]
            await self.channel_layer.group_send(group_name, {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'timestamp': message_obj.timestamp.isoformat()
            })
        except User.DoesNotExist:
            logger.error(f"User {receiver_username} doesn’t exist")

    async def handle_typing(self, data):
        """Show typing indicators in private chats"""
        is_typing = data.get('is_typing', False)
        sender = self.user.username
        receiver_username = data.get('receiver')

        if not receiver_username:
            logger.warning("No receiver specified")
            return
            
        if receiver_username not in self.private_groups:
            # Initialize the chat group if it doesn't exist
            await self.handle_start_chat({'receiver': receiver_username})

        group_name = self.private_groups[receiver_username]
        await self.channel_layer.group_send(group_name, {
            'type': 'typing_indicator',
            'sender': sender,
            'is_typing': is_typing
        })
        logger.debug(f"{sender} is typing: {is_typing} in {group_name}")

    async def chat_message(self, event):
        """Relay chat messages to the client"""
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp']
        }))

    async def typing_indicator(self, event):
        """Relay typing indicators to the client"""
        await self.send(text_data=json.dumps({
            'type': 'typing_indicator',
            'sender': event['sender'],
            'is_typing': event['is_typing']
        }))

    async def user_list_update(self, event):
        """Send the updated user list to the client"""
        users = await self.get_all_users()
        logger.debug(f"Sending user list to {self.user.username}: {users}")
        await self.send(text_data=json.dumps({
            'type': 'user_list',
            'users': users,
            'timestamp': datetime.now().isoformat()
        }))

    async def send_user_list(self):
        """Send the initial user list to the newly connected client"""
        users = await self.get_all_users()
        logger.debug(f"Initial user list for {self.user.username}: {users}")
        await self.send(text_data=json.dumps({
            'type': 'user_list',
            'users': users,
            'timestamp': datetime.now().isoformat()
        }))

    @database_sync_to_async
    def update_user_status(self, status):
        """Update the user’s online status in the database"""
        from .models import UserProfile
        try:
            profile, created = UserProfile.objects.get_or_create(user=self.user, defaults={'is_online': status})
            if not created:
                old_status = profile.is_online
                profile.is_online = status
                profile.save()
                logger.info(f"{self.user.username} status changed: {old_status} -> {status}")
            else:
                logger.info(f"Created profile for {self.user.username} with status {status}")
            return profile.is_online
        except Exception as e:
            logger.error(f"Failed to update {self.user.username} status: {str(e)}")
            return False

    @database_sync_to_async
    def save_message(self, content, receiver):
        """Save a chat message to the database"""
        from .models import Message
        return Message.objects.create(
            sender=self.user,
            receiver=receiver,
            content=content
        )

    @database_sync_to_async
    def get_all_users(self):
        """Get a list of all users and their online status"""
        from django.contrib.auth.models import User
        from .models import UserProfile
        users = User.objects.exclude(is_superuser=True)  # Exclude superusers if desired
        user_list = []
        for user in users:
            try:
                profile = UserProfile.objects.get(user=user)
                is_online = profile.is_online
            except UserProfile.DoesNotExist:
                is_online = False
            user_list.append({
                'username': user.username,
                'is_online': is_online
            })
        logger.debug(f"User list fetched: {user_list}")
        return user_list

    def _generate_group_name(self, other_username):
        """Create a unique name for private chat groups"""
        return f"chat_{min(self.user.username, other_username)}_{max(self.user.username, other_username)}"

    async def _broadcast_user_list_update(self):
        """Notify all connected users of an updated user list"""
        logger.debug(f"Broadcasting user list update to {self.lobby_group_name}")
        await self.channel_layer.group_send(self.lobby_group_name, {
            'type': 'user_list_update'
        })

# Signal handler for Django logout
@receiver(user_logged_out)
def update_user_status_on_logout(sender, user, request, **kwargs):
    """Update user status and notify others when a user logs out"""
    from channels.layers import get_channel_layer
    from .models import UserProfile
    
    try:
        profile, created = UserProfile.objects.get_or_create(user=user, defaults={'is_online': False})
        if not created and profile.is_online:
            profile.is_online = False
            profile.save()
            logger.info(f"{user.username} logged out, status updated to offline")

            # Broadcast the update to all connected clients
            channel_layer = get_channel_layer()
            if channel_layer:
                async def broadcast():
                    await channel_layer.group_send('chat_lobby', {
                        'type': 'user_list_update'
                    })
                async_to_sync(broadcast)()
    except Exception as e:
        logger.error(f"Error handling logout for {user.username}: {str(e)}")