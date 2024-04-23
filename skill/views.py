from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework import status
from .serializers import SkillSerializer, UserSkillSerializer
from .models import Skill, UserSkill, SkillEvaluation
from django.core.exceptions import ObjectDoesNotExist
from api_auth.models import User


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


@api_view(['GET'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def list_by_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        user = None

    if not isinstance(user, User):
        raise TypeError('User is not found.')

    user_skills = UserSkill.objects.filter(user=user).select_related('skill')

    serializer = UserSkillSerializer(user_skills, many=True, context={'request': request})

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', 'DELETE'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def evaluate(request, link_id):
    try:
        user_skill = UserSkill.objects.get(pk=link_id)
    except ObjectDoesNotExist:
        user_skill = None

    if not isinstance(user_skill, UserSkill):
        raise TypeError('UserSkill is not found.')

    try:
        existed_skill_evaluation = SkillEvaluation.objects.get(user=request.user, link=user_skill)
    except ObjectDoesNotExist:
        existed_skill_evaluation = None

    if request.method == 'POST':
        if isinstance(existed_skill_evaluation, UserSkill):
            raise TypeError('SkillEvaluation already exists.')

        skill_evaluation = SkillEvaluation(link=user_skill, user=request.user)
        skill_evaluation.save()

        return Response({'status': True}, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        if not isinstance(existed_skill_evaluation, SkillEvaluation):
            raise TypeError('SkillEvaluation is not found.')

        existed_skill_evaluation.delete()
        return Response({'status': True}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'status': False}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
