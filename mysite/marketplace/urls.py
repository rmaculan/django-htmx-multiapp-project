from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('items/', views.item_list, name='item_list'),
    path('items/<int:item_id>/', views.item_detail, name='item_detail'),
    path('<int:question_id>/', views.question_detail, name='question_detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]