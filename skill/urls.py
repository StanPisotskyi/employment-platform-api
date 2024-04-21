from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_or_add),
    path('/<int:id>/handle', views.assign_or_remove)
]
