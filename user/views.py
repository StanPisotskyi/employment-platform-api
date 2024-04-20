from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from account.serializers import UserSerializer
from api_auth.models import User
from django.db.models.functions import Concat
from django.db.models import F, Value, CharField


@api_view(['GET'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def get_list_by_search(request):
    search = request.GET.get('search', '')
    users = None

    if search != '':
        try:
            users = (User
                     .objects
                     .annotate(
                full_name=Concat(
                    F('first_name'),
                    Value(' '),
                    F('last_name'),
                    output_field=CharField()
                )
            ).filter(full_name__icontains=search).order_by('full_name'))
        except User.DoesNotExist:
            users = None

    serializer = UserSerializer(users, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
