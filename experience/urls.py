from django.urls import path
from . import views

urlpatterns = [
    path('', views.add),
    path('/<int:id>/user', views.get_user_experience_data),
    path('/<int:id>', views.handle_one_by_id)
]