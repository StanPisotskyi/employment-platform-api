from django.db import models
from api_auth.models import User
from django.utils.timezone import now


class ChatManager(models.Manager):
    pass


class ChatUserManager(models.Manager):
    pass


class Chat(models.Model):
    created_at = models.DateTimeField(null=False, blank=False, default=now)

    REQUIRED_FIELDS = ['created_at']

    objects = ChatManager()

    def __str__(self):
        return self.id


class ChatUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, null=False)

    REQUIRED_FIELDS = ['user', 'chat']

    objects = ChatUserManager()

    def __str__(self):
        return self.id


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(null=False, blank=False, default=now)
    text = models.TextField(null=False, blank=False)
    is_read = models.BooleanField(null=False, blank=False)

    REQUIRED_FIELDS = ['author', 'chat', 'created_at', 'text', 'is_read']

    objects = ChatUserManager()

    def __str__(self):
        return self.id
