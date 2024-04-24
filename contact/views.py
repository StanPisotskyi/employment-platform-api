from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework import status
from api_auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Contact, STATUS_WAITING
from .serializers import ContactSerializer


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def invite(request, target_id):
    try:
        target = User.objects.get(pk=target_id)
    except ObjectDoesNotExist:
        target = None

    if not isinstance(target, User):
        raise TypeError('Target is not found.')

    if target.id == request.user.id:
        raise TypeError('Target and logged-in users is the same person.')

    try:
        existed_contact = Contact.objects.get(target=target, initiator=request.user)
    except ObjectDoesNotExist:
        existed_contact = None

    if isinstance(existed_contact, Contact):
        raise TypeError('Contact is already created.')

    contact = Contact(target=target, initiator=request.user, status=STATUS_WAITING)
    contact.save()

    serializer = ContactSerializer(contact)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
