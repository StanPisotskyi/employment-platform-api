from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api_auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Contact, STATUS_WAITING, STATUS_CONFIRMED, STATUS_BANNED
from .serializers import ContactSerializer
from django.db.models import Q


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


@api_view(['GET'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def list_of_confirmed_contacts(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        user = None

    if not isinstance(user, User):
        raise TypeError('User is not found.')

    try:
        contacts = Contact.objects.filter((Q(initiator=user) | Q(target=user)), status=STATUS_CONFIRMED).order_by('-id')
    except Contact.DoesNotExist:
        contacts = None

    serializer = ContactSerializer(contacts, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def ban(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        user = None

    if not isinstance(user, User):
        raise TypeError('User is not found.')

    try:
        contact = Contact.objects.get((Q(initiator=user) & Q(target=request.user)) |
                                      (Q(initiator=request.user) & Q(target=user)))
    except ObjectDoesNotExist:
        contact = None

    if not isinstance(contact, Contact):
        raise TypeError('Contact to confirm is not found.')

    contact.status = STATUS_BANNED
    contact.save()

    serializer = ContactSerializer(contact)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def remove(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        user = None

    if not isinstance(user, User):
        raise TypeError('User is not found.')

    try:
        contact = Contact.objects.get(((Q(initiator=user) & Q(target=request.user)) |
                                      (Q(initiator=request.user) & Q(target=user))), status=STATUS_CONFIRMED)
    except ObjectDoesNotExist:
        contact = None

    if not isinstance(contact, Contact):
        raise TypeError('Contact to confirm is not found.')

    contact.delete()

    return Response({'status': True}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def list_of_recommended_contacts(request):
    try:
        contacts = Contact.objects.raw('SELECT c1.id, c1.initiator_id, c1.target_id FROM contact_contact c1 LEFT JOIN contact_contact c2 ON c2.initiator_id = c1.initiator_id LEFT JOIN contact_contact c3 ON c3.target_id = c1.initiator_id LEFT JOIN contact_contact c4 ON c4.initiator_id = c1.target_id LEFT JOIN contact_contact c5 ON c5.target_id = c1.target_id WHERE c1.initiator_id <> %s AND c1.target_id <> %s AND c1.status = %s AND (c2.target_id = %s OR c3.initiator_id =%s OR c4.target_id = %s OR c5.initiator_id = %s) GROUP BY c1.id', [request.user.id, request.user.id, STATUS_CONFIRMED, request.user.id, request.user.id, request.user.id, request.user.id])
    except ObjectDoesNotExist:
        contacts = None

    serializer = ContactSerializer(contacts, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
