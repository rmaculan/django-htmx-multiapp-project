from django.contrib import admin
from .models import BlogCustomUser, BloggerProfile, Post, Comment, Like

# Register your models here.
admin.site.register([BlogCustomUser, BloggerProfile, Post, Comment, Like])