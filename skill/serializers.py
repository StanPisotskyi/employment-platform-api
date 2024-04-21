from rest_framework import serializers
from .models import Skill


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

    class Meta:
        model = Skill
        fields = ['id', 'skill',]
