from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from .serializers import CompanySerializer, CompanyUserSerializer, CompanyUsersSerializer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Company, CompanyUser
from .permissions import IsCompanyUser, IsAllowedToWorkWithCompanyData


@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def list_and_create(request):
    if request.method == 'GET':
        search = request.GET.get('search', '')
        companies = None

        if search != '':
            try:
                companies = Company.objects.filter(title__istartswith=search).order_by('title')
            except Company.DoesNotExist:
                companies = None

        serializer = CompanySerializer(companies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CompanySerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({'status': False}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'PUT', 'DELETE'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAllowedToWorkWithCompanyData])
def handle_one_by_id(request, id):
    company = Company.objects.get(pk=id)

    if request.method == 'GET':
        serializer = CompanySerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        company.delete()
        return Response({'status': True}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'status': False}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST', 'DELETE'])
@renderer_classes([JSONRenderer])
@permission_classes([IsCompanyUser])
def handle_company_user(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CompanyUserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        data = JSONParser().parse(request)
        serializer = CompanyUserSerializer()

        return Response(serializer.remove(data), status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'status': False}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
@permission_classes([IsCompanyUser])
def get_company_users(request, id):
    company = Company.objects.get(pk=id)
    company_users = CompanyUser.objects.filter(company=company).select_related('user')

    serializer = CompanyUsersSerializer(company_users, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)