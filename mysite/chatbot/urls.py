from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chat_view, name='chat_view'),
    path('chats/', views.chat_list, name='chat_list'),
    path('chats/<int:pk>/', views.chat_detail, name='chat_detail'),
    path('chats/create/', views.create_chat, name='create_chat'),
]
