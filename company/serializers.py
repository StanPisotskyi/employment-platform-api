from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    about = serializers.CharField(max_length=255)
    establish_date = serializers.IntegerField()

    class Meta:
        model = Company
        fields = ['id', 'title', 'about', 'establish_date']

    def create(self, validated_data):
        return Company.objects.create_company(**validated_data)