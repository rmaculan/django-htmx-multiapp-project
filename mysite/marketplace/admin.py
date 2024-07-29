from django.contrib import admin

# Register your models here.
from .models import Item, CategoryModel, Review, UserProfile, Conversation,UserMessage,  Question

admin.site.register([
    Item, 
    CategoryModel, 
    Review, 
    UserProfile, 
    Conversation, 
    UserMessage, 
    Question
    ])