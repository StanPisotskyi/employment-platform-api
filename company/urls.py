from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_and_create),
    path('/<int:id>', views.handle_one_by_id),
    path('/<int:id>/users', views.get_company_users),
    path('/user', views.handle_company_user),
]