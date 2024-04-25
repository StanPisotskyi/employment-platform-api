from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api_auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Contact, STATUS_WAITING, STATUS_CONFIRMED
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


@api_view(['GET'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def get_invitations(request):
    try:
        invitations = Contact.objects.filter(target=request.user, status=STATUS_WAITING).order_by('-id')
    except Contact.DoesNotExist:
        invitations = None

    serializer = ContactSerializer(invitations, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def confirm(request, initiator_id):
    try:
        initiator = User.objects.get(pk=initiator_id)
    except ObjectDoesNotExist:
        initiator = None

    if not isinstance(initiator, User):
        raise TypeError('Initiator is not found.')

    try:
        existed_contact = Contact.objects.get(initiator=initiator, target=request.user, status=STATUS_WAITING)
    except ObjectDoesNotExist:
        existed_contact = None

    if not isinstance(existed_contact, Contact):
        raise TypeError('Contact to confirm is not found.')

    existed_contact.status = STATUS_CONFIRMED
    existed_contact.save()

    serializer = ContactSerializer(existed_contact)
    return Response(serializer.data, status=status.HTTP_200_OK)
