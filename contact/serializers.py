from rest_framework import serializers
from account.serializers import UserSerializer
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    initiator = UserSerializer()
    target = UserSerializer()
    status = serializers.CharField(max_length=255)

    class Meta:
        model = Contact
        fields = ['id', 'initiator', 'target', 'status',]