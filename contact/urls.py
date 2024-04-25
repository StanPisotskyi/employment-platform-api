from django.urls import path
from . import views

urlpatterns = [
    path('/<int:target_id>/invite', views.invite),
    path('/invitations', views.get_invitations),
    path('/<int:initiator_id>/confirm', views.confirm)
]
