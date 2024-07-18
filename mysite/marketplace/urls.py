from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('search_results/', views.search_items),
    path('item_form/', views.create_item, name='create_item'),  # Renamed from 'item_name' to 'create_item'
    path('item_detail/', views.item_list, name='item_list'),
    path('item_detail/<int:item_id>/', views.item_detail, name='item_detail'),
    path('item_confirm_delete/<int:item_id>/', views.delete_item),
    path('<int:question_id>/', views.question_detail, name='question_detail'),
    path('question_form/', views.create_question),
    path('question_list/', views.question_list),
    path('question_confirm_delete/<int:question_id>/', views.delete_question),
    # path('<int:question_id>/results/', views.results, name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]