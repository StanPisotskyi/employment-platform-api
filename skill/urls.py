from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_or_add),
    path('/<int:id>/handle', views.assign_or_remove),
    path('/<int:user_id>/user', views.list_by_user)
]
