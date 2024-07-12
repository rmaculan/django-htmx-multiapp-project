from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('item_detail/', views.item_list, name='item_list'),
    path('item_detail/<int:item_id>/', views.item_detail, name='item_detail'),
    path('<int:question_id>/', views.question_detail, name='question_detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]