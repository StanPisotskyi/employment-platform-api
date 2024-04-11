from rest_framework import serializers
from .models import Company, CompanyUser


class CompanySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    website = serializers.CharField(max_length=255)
    about = serializers.CharField(max_length=255)
    establish_year = serializers.IntegerField()
    user = serializers.HiddenField(default=None)

    class Meta:
        model = Company
        fields = ['id', 'title', 'website', 'about', 'establish_year', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Company.objects.create_company(**validated_data)


class CompanyUserSerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(read_only=True)
    company_id = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CompanyUser
        fields = ['status', 'company_id', 'user_id']

    def create(self, validated_data):
        return CompanyUser.objects.add_company_user(**validated_data)

    def remove(self, validated_data):
        return CompanyUser.objects.remove_company_user(**validated_data)