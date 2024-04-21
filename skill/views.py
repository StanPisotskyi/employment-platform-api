from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework import status
from .serializers import SkillSerializer, UserSkillSerializer
from .models import Skill, UserSkill
from django.core.exceptions import ObjectDoesNotExist


@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def list_or_add(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SkillSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        search = request.GET.get('search', '')
        skills = None

        if search != '':
            try:
                skills = Skill.objects.filter(title__istartswith=search).order_by('title')
            except Skill.DoesNotExist:
                skills = None

        serializer = SkillSerializer(skills, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'status': False}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST', 'DELETE'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def assign_or_remove(request, id):
    try:
        skill = Skill.objects.get(pk=id)
    except ObjectDoesNotExist:
        skill = None

    if not isinstance(skill, Skill):
        raise TypeError('Skill is not found.')

    try:
        existed_user_skill = UserSkill.objects.get(user=request.user, skill=skill)
    except ObjectDoesNotExist:
        existed_user_skill = None

    if request.method == 'POST':
        if isinstance(existed_user_skill, UserSkill):
            raise TypeError('UserSkill already exists.')

        user_skill = UserSkill(skill=skill, user=request.user)
        user_skill.save()

        serializer = UserSkillSerializer(user_skill)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        if not isinstance(existed_user_skill, UserSkill):
            raise TypeError('UserSkill is not found.')

        existed_user_skill.delete()
        return Response({'status': True}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'status': False}, status=status.HTTP_405_METHOD_NOT_ALLOWED)