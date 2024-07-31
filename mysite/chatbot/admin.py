from django.contrib import admin
from .models import ChatbotUser, ChatbotProfile, AIChat, Message

# Register your models here.
admin.site.register([ChatbotUser, ChatbotProfile, AIChat, Message])
