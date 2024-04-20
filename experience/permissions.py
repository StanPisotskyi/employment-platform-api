from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist
from .models import Experience


class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        experience_id = view.kwargs.get('id', None)

        try:
            experience = Experience.objects.get(pk=experience_id, user=request.user)
        except ObjectDoesNotExist:
            experience = None

        return bool(request.user and request.user.is_authenticated and isinstance(experience, Experience))