from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from .serializers import ExperienceAddSerializer, ExperienceGetSerializer
from rest_framework import status
from api_auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Experience
from .permissions import IsOwner


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def add(request):
    data = JSONParser().parse(request)
    serializer = ExperienceAddSerializer(data=data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def get_user_experience_data(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        user = None

    if not isinstance(user, User):
        raise TypeError('User is not found.')

    try:
        experience = Experience.objects.filter(user=user).order_by('-date_from')
    except Experience.DoesNotExist:
        experience = None

    serializer = ExperienceGetSerializer(experience, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT', 'DELETE'])
@renderer_classes([JSONRenderer])
@permission_classes([IsOwner])
def handle_one_by_id(request, id):
    try:
        experience = Experience.objects.get(pk=id, user=request.user)
    except ObjectDoesNotExist:
        experience = None

    if not isinstance(experience, Experience):
        raise TypeError('Experience is not found.')

    if request.method == 'PUT':
        serializer = ExperienceAddSerializer(experience, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        experience.delete()
        return Response({'status': True}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'status': False}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
