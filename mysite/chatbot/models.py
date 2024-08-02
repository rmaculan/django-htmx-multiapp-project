from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext as _
from django.conf import settings

class ChatbotUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_("The groups this user belongs to."),
        related_name="chatbot_user_groups",
        related_query_name="chatbot_user",
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="chatbot_user_permissions",
        related_query_name="chatbot_user",
    )

class ChatbotProfile(models.Model):
    user = models.OneToOneField(
        ChatbotUser, 
        on_delete=models.CASCADE
    )
    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True, 
        null=True
    )
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    is_chatbot_author = models.BooleanField(default=False)

class AIChat(models.Model):
    title = models.CharField(max_length=200)
    user_message = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    thumbnail = models.ImageField(
        upload_to='thumbnails/', 
        blank=True, 
        null=True
    )
    
    def __str__(self):
        return self.title

class Message(models.Model):
    user_message = models.TextField()
    bot_message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    aichat = models.ForeignKey(
        AIChat, 
        on_delete=models.CASCADE,
        null=False  # Allow null values
    )
    chat_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        null=False  # Ensure every message is linked to a user
    )

    def __str__(self):
        return self.user_message

class Chatbot(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail = models.ImageField(
        upload_to='thumbnails/', 
        blank=True, 
        null=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

