from django.db import models
from api_auth.models import User

STATUS_OWNER = 'owner'


class CompanyManager(models.Manager):
    def create_company(self, title, about, establish_date, user):
        if title is None:
            raise TypeError('Company must have a title.')
        if about is None:
            raise TypeError('Company must have an about.')
        if establish_date is None:
            raise TypeError('Company must have an establish_date.')

        company = self.model(title=title, about=about, establish_date=establish_date)
        company_user = self.model.objects.create(company=company, user=user, status=STATUS_OWNER)

        company.save()
        company_user.save()

        return company


class Company(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    about = models.TextField(null=False, blank=False)
    establish_date = models.IntegerField(null=False, blank=False)

    REQUIRED_FIELDS = ['title', 'about', 'establish_date']

    objects = CompanyManager()

    def __str__(self):
        return self.title


class CompanyUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='company_user_set')
    company = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='company_company_set')
    status = models.CharField(max_length=255, null=False, blank=False)

    REQUIRED_FIELDS = ['user', 'company', 'status']

    class Meta:
        unique_together = (('user', 'company'),)

    def __str__(self):
        return self.status

