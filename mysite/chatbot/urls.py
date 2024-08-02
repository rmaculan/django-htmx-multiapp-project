from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.index, name='index'),
    path('chats/', views.chat_list, name='chat_list'),
    path('chats/<int:pk>/', views.chat_view, name='chat_detail'),
    path('chats/create/<int:pk>/', views.create_chat, name='create_chat'),
]
