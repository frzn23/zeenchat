# chatapp/models.py
import base64
from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import hashlib

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
    # Create a proper 32-byte key from SECRET_KEY
    key_material = settings.SECRET_KEY.encode()
    # Use SHA256 to ensure we get exactly 32 bytes
    key_bytes = hashlib.sha256(key_material).digest()
    # Base64 encode to get the proper format for Fernet
    key = base64.urlsafe_b64encode(key_bytes)
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
        if not self._content:
            return ""
        try:
            cipher = get_cipher()
            return cipher.decrypt(self._content.encode()).decode()
        except Exception:
            # If decryption fails, return the original content
            # This helps with any existing unencrypted data
            return self._content

    @content.setter
    def content(self, raw_text):
        """Encrypt message before saving."""
        if not raw_text:
            self._content = ""
            return
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

    