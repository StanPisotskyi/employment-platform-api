from django.urls import path
from . import views

urlpatterns = [
    path('', views.create),
    path('/<int:id>', views.get_one_by_id),
    path('/<str:search>/search', views.get_list_by_search),
    path('/add-company-user', views.add_company_user)
]