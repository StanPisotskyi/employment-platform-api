from django.urls import path
from . import views

urlpatterns = [
    path('/<str:search>/search', views.get_list_by_search),
]