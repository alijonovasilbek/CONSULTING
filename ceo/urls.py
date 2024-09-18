from  ceo import views
from django.urls import path


urlpatterns = [
    path('ceo/',views.ceo,name='ceo'),
    path('send-message/<int:receiver_id>/', views.send_message, name='send_message'),
    path('messages/', views.message_list, name='message_list'),
    path('message/<int:message_id>/', views.message_detail, name='message_detail'),
    path('message/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('message/deleteceo/<int:message_id>/', views.delete_message_ceo, name='delete_message_ceo'),
    path('messagesceo/',views.message_list_ceo,name='message_list_ceo'),
    path('dashboard/<str:company_code>/', views.user_dashboard, name='user_dashboard'),
    path('message/send-to-all/', views.send_message_all, name='send_message_to_all'),
    path('toggle_user_active/', views.toggle_user_active, name='toggle_user_active')

]
