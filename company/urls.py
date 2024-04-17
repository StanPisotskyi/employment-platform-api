from django.urls import path
from . import views

urlpatterns = [
    path('', views.create),
    path('/<int:id>', views.handle_one_by_id),
    path('/<str:search>/search', views.get_list_by_search),
    path('/<int:id>/users', views.get_company_users),
    path('/add-company-user', views.add_company_user),
    path('/remove-company-user', views.remove_company_user)
]