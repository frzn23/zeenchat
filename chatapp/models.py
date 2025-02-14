# chatapp/models.py
from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import base64
from django.conf import settings

# Generate a key once and store it securely
KEY = settings.SECRET_KEY[:32]  # Use a strong, static key instead of this

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
