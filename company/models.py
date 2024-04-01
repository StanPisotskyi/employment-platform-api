from django.db import models
from api_auth.models import User


class Company(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    about = models.TextField(null=False, blank=False)
    establish_date = models.DateField(null=False, blank=False)

    REQUIRED_FIELDS = ['title', 'about', 'establish_date']

    def __str__(self):
        return self.title