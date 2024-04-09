from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from .serializers import CompanySerializer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Company
from .permissions import IsCompanyUser


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def create(request):
    data = JSONParser().parse(request)
    serializer = CompanySerializer(data=data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def get_one_by_id(request, id):
    company = Company.objects.get(pk=id)
    serializer = CompanySerializer(company)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def get_list_by_search(request, search):
    try:
        companies = Company.objects.filter(title__istartswith=search).order_by('title')
    except Company.DoesNotExist:
        companies = None

    serializer = CompanySerializer(companies, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsCompanyUser])
def add_company_user(request):
    return Response({'status': True}, status=status.HTTP_201_CREATED)