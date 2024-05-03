from django.db import models
from api_auth.models import User
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist


class ChatManager(models.Manager):
    def create(self, target_id, user):
        if target_id is None:
            raise TypeError('Chat must have a target user.')

        try:
            target = User.objects.get(pk=target_id)
        except ObjectDoesNotExist:
            target = None

        if not isinstance(target, User):
            raise TypeError('Target user is not found.')

        if target.id == user.id:
            raise TypeError('Target and logged-in user is the same person.')

        user_chats_ids = []
        user_chats = ChatUser.objects.filter(user=user).select_related('chat')

        for user_chat in user_chats:
            user_chats_ids.append(user_chat.chat.id)

        try:
            existed_link = ChatUser.objects.get(user=target, chat_id__in=user_chats_ids)
        except ObjectDoesNotExist:
            existed_link = None

        if isinstance(existed_link, ChatUser):
            raise TypeError('Chat is already created.')

        chat = Chat()
        chat_user = ChatUser(chat=chat, user=user)
        chat_target = ChatUser(chat=chat, user=target)

        chat.save()
        chat_user.save()
        chat_target.save()

        return chat


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
