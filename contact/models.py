from django.db import models
from api_auth.models import User

STATUS_WAITING = 'waiting'
STATUS_CONFIRMED = 'confirmed'
STATUS_BANNED = 'banned'


class ContactManager(models.Manager):
    pass


class Contact(models.Model):
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='contact_initiator_set')
    target = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='contact_target_set')
    status = models.CharField(max_length=255, null=False, blank=False)

    REQUIRED_FIELDS = ['initiator', 'target', 'status']

    objects = ContactManager()

    class Meta:
        unique_together = (('initiator', 'target'),)

    def __str__(self):
        return str(self.id)
