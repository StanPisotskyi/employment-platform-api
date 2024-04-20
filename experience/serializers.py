from rest_framework import serializers
from .models import Experience
from account.serializers import UserSerializer
from company.serializers import CompanySerializer


class ExperienceAddSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    company_id = serializers.IntegerField(write_only=True, default=None)
    company_title = serializers.CharField(max_length=255)
    position = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255, default=None)
    date_from = serializers.DateField(format="%Y-%m-%d")
    date_to = serializers.DateField(format="%Y-%m-%d", default=None)
    user = serializers.HiddenField(default=None, write_only=True)

    class Meta:
        model = Experience
        fields = ['id', 'company_id', 'company_title', 'position', 'description', 'date_from', 'date_to', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Experience.objects.add_experience(**validated_data)

    def update(self, instance, validated_data):
        validated_data['experience'] = instance
        del validated_data['user']
        return Experience.objects.update_experience(**validated_data)


class ExperienceGetSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    company = CompanySerializer(read_only=True)
    company_title = serializers.CharField(max_length=255)
    position = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255, default=None)
    date_from = serializers.DateField(format="%Y-%m-%d")
    date_to = serializers.DateField(format="%Y-%m-%d", default=None)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Experience
        fields = ['id', 'company', 'company_title', 'position', 'description', 'date_from', 'date_to', 'user']
