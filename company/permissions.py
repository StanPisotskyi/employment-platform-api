from rest_framework import permissions
from company.models import CompanyUser
import json
from django.core.exceptions import ObjectDoesNotExist


class IsCompanyUser(permissions.BasePermission):

    def has_permission(self, request, view):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        company_user = None

        if request.user and 'firm_id' in body:
            try:
                company_user = CompanyUser.objects.get(company=body['firm_id'], user=request.user)
            except ObjectDoesNotExist:
                company_user = None

        return bool(request.user and request.user.is_authenticated and isinstance(company_user, CompanyUser))