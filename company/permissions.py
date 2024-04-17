from rest_framework import permissions
from company.models import CompanyUser, STATUS_OWNER
import json
from django.core.exceptions import ObjectDoesNotExist


class IsCompanyUser(permissions.BasePermission):

    def has_permission(self, request, view):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        company_user = None

        if request.user and 'company_id' in body:
            try:
                company_user = CompanyUser.objects.get(company=body['company_id'], user=request.user)
            except ObjectDoesNotExist:
                company_user = None

        return bool(request.user and request.user.is_authenticated and isinstance(company_user, CompanyUser))


class IsAllowedToWorkWithCompanyData(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return bool(request.user and request.user.is_authenticated)

        company_id = view.kwargs.get('id', None)

        try:
            company_user = CompanyUser.objects.get(company=company_id, user=request.user)
        except ObjectDoesNotExist:
            company_user = None

        if request.method == 'PUT':
            return bool(request.user and request.user.is_authenticated and isinstance(company_user, CompanyUser))
        elif request.method == 'DELETE':
            return company_user.status == STATUS_OWNER
        else:
            return False