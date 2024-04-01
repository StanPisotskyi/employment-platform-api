from django.db import models
from api_auth.models import User
from company.models import Company


class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    company_title = models.CharField(max_length=255, null=False, blank=False)
    position = models.CharField(max_length=255, null=False, blank=False)
    description = models.CharField(max_length=255, null=True, blank=True)
    date_from = models.DateField(null=False, blank=False)
    date_to = models.DateField(auto_now=True)

    REQUIRED_FIELDS = ['company_title', 'position', 'date_from']

    def __str__(self):
        return self.company_title
