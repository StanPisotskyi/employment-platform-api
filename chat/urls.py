from django.urls import path
from . import views

urlpatterns = [
    path('', views.handle_chats),
    path('/<int:chat_id>/messages', views.handle_messages)
]
