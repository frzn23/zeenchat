# chatapp/models.py
import base64
from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Generate a key once and store it securely
KEY = settings.SECRET_KEY[:32]  # Use a strong, static key instead of this

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(default=timezone.now)
    
    class Meta:
        indexes = [
            models.Index(fields=['is_online']),
            models.Index(fields=['last_seen'])
        ]

def get_cipher():
    key = base64.urlsafe_b64encode(KEY.encode())  # Ensure 32-byte key
    return Fernet(key)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    
    _content = models.TextField(db_column='content', default="")  # Store encrypted content
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        return f'{self.sender} to {self.receiver}'

    @property
    def content(self):
        """Decrypt message before serving."""
        cipher = get_cipher()
        return cipher.decrypt(self._content.encode()).decode()

    @content.setter
    def content(self, raw_text):
        """Encrypt message before saving."""
        cipher = get_cipher()
        self._content = cipher.encrypt(raw_text.encode()).decode()

class FriendRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")   # db value(not translated), display name(translatable)
        ACCEPTED = "accepted", _("Accepted")

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_request')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_request')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)


    def __str__(self):
        return f'{self.sender} to {self.receiver}'

    