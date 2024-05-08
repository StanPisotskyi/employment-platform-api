from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.parsers import JSONParser
from .serializers import ChatSerializer, ChatGetSerializer, MessageSerializer
from .models import Chat
from django.core.exceptions import ObjectDoesNotExist


@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def handle_chats(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ChatSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    if request.method == 'GET':
        try:
            chats = Chat.objects.raw('SELECT c.id, c.created_at, CONCAT(u.first_name, " ", u.last_name) as title FROM chat_chat c JOIN chat_chatuser cu ON cu.chat_id = c.id AND cu.user_id = %s JOIN chat_chatuser cu2 ON cu2.chat_id = cu.chat_id AND cu2.user_id <> cu.user_id JOIN api_auth_user u ON u.id = cu2.user_id ORDER BY c.created_at DESC', [request.user.id])
        except Chat.DoesNotExist:
            chats = None

        serializer = ChatGetSerializer(chats, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'status': False}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def handle_messages(request, chat_id):
    try:
        chat = Chat.objects.get(pk=chat_id)
    except ObjectDoesNotExist:
        chat = None

    if not isinstance(chat, Chat):
        raise TypeError('Chat is not found.')

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data, context={'request': request, 'chat': chat})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({'status': False}, status=status.HTTP_405_METHOD_NOT_ALLOWED)