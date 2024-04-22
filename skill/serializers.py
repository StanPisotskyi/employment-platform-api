from rest_framework import serializers
from .models import Skill, SkillEvaluation
from django.core.exceptions import ObjectDoesNotExist


class SkillSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)

    class Meta:
        model = Skill
        fields = ['id', 'title',]

    def create(self, validated_data):
        return Skill.objects.create(**validated_data)


class UserSkillSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    skill = SkillSerializer(read_only=True)
    is_voted = serializers.SerializerMethodField()
    votes = serializers.SerializerMethodField()

    def get_is_voted(self, obj):
        try:
            skill_evaluation = SkillEvaluation.objects.get(link=obj, user=self.context['request'].user)
        except ObjectDoesNotExist:
            skill_evaluation = None

        return bool(isinstance(skill_evaluation, SkillEvaluation))

    def get_votes(self, obj):
        return SkillEvaluation.objects.filter(link=obj).count()

    class Meta:
        model = Skill
        fields = ['id', 'skill', 'is_voted', 'votes',]
