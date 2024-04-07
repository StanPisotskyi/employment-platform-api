from rest_framework import serializers
from .models import Company


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