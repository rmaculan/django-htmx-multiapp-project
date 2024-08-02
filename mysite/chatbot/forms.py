from django import forms
from .models import AIChat

class ChatForm(forms.ModelForm):
    class Meta:
        model = AIChat
        fields = ['title', 'user_message']


