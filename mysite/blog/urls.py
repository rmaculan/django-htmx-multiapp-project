from django.urls import path
from . import views

urlpatterns = [
    path('', views.read_blog_posts, name='index'),
    path('<int:post_id>/', views.read_blog_post, name='post_detail'),
    path('create_blog_post/', views.create_blog_post, name='create_blog_post'),
]