from django.db import models
from api_auth.models import User
from company.models import Company
from django.core.exceptions import ObjectDoesNotExist


class ExperienceManager(models.Manager):
    def add_experience(self, company_id, company_title, position, description, date_from, date_to, user):
        if company_title is None:
            raise TypeError('Experience must have a company title.')
        if position is None:
            raise TypeError('Experience must have a position.')
        if date_from is None:
            raise TypeError('Experience must have a date from value.')

        company = None

        if company_id:
            try:
                company = Company.objects.get(pk=company_id)
            except ObjectDoesNotExist:
                company = None

        experience = Experience(
            user=user,
            company=company,
            company_title=company_title,
            position=position,
            description=description,
            date_from=date_from,
            date_to=date_to
        )

        experience.save()

        return experience

    def update_experience(self, company_id, company_title, position, description, date_from, date_to, experience):
        if company_title is None:
            raise TypeError('Experience must have a company title.')
        if position is None:
            raise TypeError('Experience must have a position.')
        if date_from is None:
            raise TypeError('Experience must have a date from value.')

        company = None

        if company_id:
            try:
                company = Company.objects.get(pk=company_id)
            except ObjectDoesNotExist:
                company = None

        experience.company = company
        experience.company_title = company_title
        experience.position = position
        experience.description = description
        experience.date_from = date_from
        experience.date_to = date_to

        experience.save()

        return experience


class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    company_title = models.CharField(max_length=255, null=False, blank=False)
    position = models.CharField(max_length=255, null=False, blank=False)
    description = models.CharField(max_length=255, null=True, blank=True)
    date_from = models.DateField(null=False, blank=False)
    date_to = models.DateField(null=True, blank=True)

    REQUIRED_FIELDS = ['company_title', 'position', 'date_from']

    objects = ExperienceManager()

    def __str__(self):
        return self.company_title
