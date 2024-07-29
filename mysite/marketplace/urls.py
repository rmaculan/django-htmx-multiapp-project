from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('contact_seller_form/<int:item_id>/', views.contact_seller_form, name='contact_seller_form'),
    path('mesages/', views.user_messages, name='messages'),
    path('reply_form/<int:message_id>/', views.reply_form, name='reply_form'),
    path('view_conversation/<int:message_id>/', views.view_conversation, name='view_conversation'),
    path('seller_items/', views.seller_items, name='seller_items'),
    path('search_results/', views.search_items),
    path('item_form/', views.create_item, name='create_item'),  # Renamed from 'item_name' to 'create_item'
    path('item_detail/', views.item_list, name='item_list'),
    path('update_item/<int:item_id>/', views.update_item, name='update_item'),
    path('item_detail/<int:item_id>/', views.item_detail, name='item_detail'),
    path('item_confirm_delete/<int:item_id>/', views.delete_item, name='delete_item'),
    path('<int:question_id>/', views.question_detail, name='question_detail'),
    path('question_form/', views.create_question),
    path('question_list/', views.question_list),
    path('question_confirm_delete/<int:question_id>/', views.delete_question),
    # path('<int:question_id>/results/', views.results, name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]