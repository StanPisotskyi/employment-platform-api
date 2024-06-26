from django.db import models
from api_auth.models import User
from django.db.models import Q
import validators
import re
from django.core.exceptions import ObjectDoesNotExist

STATUS_OWNER = 'owner'
STATUS_EMPLOYEE = 'employee'


class CompanyManager(models.Manager):
    def create_company(self, title, website, about, establish_year, user):
        if title is None:
            raise TypeError('Company must have a title.')
        if website is None:
            raise TypeError('Company must have a website.')
        if about is None:
            raise TypeError('Company must have an about.')
        if establish_year is None:
            raise TypeError('Company must have an establish_year.')
        if not validators.url(website):
            raise TypeError('Invalid website value.')

        url = re.compile(r"https?://(www\.)?")
        prepared_url = url.sub('', website).strip().strip('/')

        exists = Company.objects.filter(Q(title=title) | Q(website=prepared_url)).exists()

        if exists:
            raise TypeError('Company with that title and/or website already exists.')

        company = Company(title=title, website=prepared_url, about=about, establish_year=establish_year)
        company_user = CompanyUser(company=company, user=user, status=STATUS_OWNER)

        company.save()
        company_user.save()

        return company

    def update_company(self, title, website, about, establish_year, company):
        if title is None:
            raise TypeError('Company must have a title.')
        if website is None:
            raise TypeError('Company must have a website.')
        if about is None:
            raise TypeError('Company must have an about.')
        if establish_year is None:
            raise TypeError('Company must have an establish_year.')
        if not validators.url(website):
            raise TypeError('Invalid website value.')

        url = re.compile(r"https?://(www\.)?")
        prepared_url = url.sub('', website).strip().strip('/')

        exists_with_title = False
        exists_with_website = False

        if title != company.title:
            exists_with_title = Company.objects.filter(title=title).exists()

        if prepared_url != company.website:
            exists_with_website = Company.objects.filter(website=prepared_url).exists()

        if exists_with_title or exists_with_website:
            raise TypeError('Company with that title and/or website already exists.')

        company.title = title
        company.website = prepared_url
        company.about = about
        company.establish_year = establish_year
        company.save()

        return company


class CompanyUserManager(models.Manager):
    def add_company_user(self, company_id, user_id):

        try:
            user = User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            user = None

        if not isinstance(user, User):
            raise TypeError('User is not found.')

        try:
            company = Company.objects.get(pk=company_id)
        except ObjectDoesNotExist:
            company = None

        if not isinstance(company, Company):
            raise TypeError('Company is not found.')

        try:
            existed_company_user = CompanyUser.objects.get(company=company, user=user)
        except ObjectDoesNotExist:
            existed_company_user = None

        if isinstance(existed_company_user, CompanyUser):
            raise TypeError('User is already assigned to this company.')

        company_user = CompanyUser(company=company, user=user, status=STATUS_EMPLOYEE)

        company_user.save()

        return {'status': True}

    def remove_company_user(self, company_id, user_id):

        try:
            user = User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            user = None

        if not isinstance(user, User):
            raise TypeError('User is not found.')

        try:
            company = Company.objects.get(pk=company_id)
        except ObjectDoesNotExist:
            company = None

        if not isinstance(company, Company):
            raise TypeError('Company is not found.')

        try:
            company_user = CompanyUser.objects.get(company=company, user=user)
        except ObjectDoesNotExist:
            company_user = None

        if not isinstance(company_user, CompanyUser):
            raise TypeError('User is not assigned to this company.')

        company_user.delete()

        return {'status': True}


class Company(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False, db_index=True, unique=True)
    website = models.CharField(max_length=255, null=False, blank=False, db_index=True, unique=True)
    logo = models.CharField(max_length=255, null=True, blank=True)
    about = models.TextField(null=False, blank=False)
    establish_year = models.IntegerField(null=False, blank=False)

    REQUIRED_FIELDS = ['title', 'website', 'about', 'establish_year']

    objects = CompanyManager()

    def __str__(self):
        return self.title


class CompanyUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='company_user_set')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=False, related_name='company_company_set')
    status = models.CharField(max_length=255, null=False, blank=False)

    REQUIRED_FIELDS = ['user', 'company', 'status']

    objects = CompanyUserManager()

    class Meta:
        unique_together = (('user', 'company'),)

    def __str__(self):
        return self.status

