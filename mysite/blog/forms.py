from django import forms
from .models import Post, Like

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'subtitle', 'job_title','content', 'thumbnail']

class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = ['post', 'user']