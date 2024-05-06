from rest_framework import serializers
from account.serializers import UserSerializer
from .models import Chat, Message


class ChatSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    target_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'created_at', 'target_id',]

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Chat.objects.create(**validated_data)


class ChatGetSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    title = serializers.CharField(read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'created_at', 'title',]

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Chat.objects.create(**validated_data)


class MessageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateField(format="%Y-%m-%d", read_only=True)
    chat = ChatSerializer(read_only=True)
    author = UserSerializer(read_only=True)
    text = serializers.CharField(max_length=255)
    is_read = serializers.BooleanField()

    class Meta:
        model = Message
        fields = ['id', 'created_at', 'chat', 'author', 'text', 'is_read',]
