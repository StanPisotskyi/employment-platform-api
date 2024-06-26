from django.urls import path
from . import views

urlpatterns = [
    path('/<int:target_id>/invite', views.invite),
    path('/invitations', views.get_invitations),
    path('/<int:initiator_id>/confirm', views.confirm),
    path('/<int:user_id>/confirmed', views.list_of_confirmed_contacts),
    path('/<int:user_id>/ban', views.ban),
    path('/<int:user_id>/remove', views.remove),
    path('/recommended', views.list_of_recommended_contacts)
]
