from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.read_blog_posts, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('my_posts/', views.read_my_posts, name='my_posts'),
    path('<int:post_id>/', views.read_blog_post, name='post_detail'),
    path('create_blog_post/', views.create_blog_post, name='create_blog_post'),
    path('<int:post_id>/update/', views.update_blog_post, name='update_blog_post'),
    path('<int:post_id>/delete/', views.delete_blog_post, name='delete_blog_post'),
    path('<int:post_id>/like/', views.like_post, name='like_post'),
]