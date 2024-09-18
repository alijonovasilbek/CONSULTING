

from django.urls import path
from . import  views

urlpatterns = [
    path('index1/', views.index1, name='index1'),
    path('user/', views.get_all_users, name='user'),
    path('test/', views.get_all_tests, name='test'),
    path('participation/', views.get_all_participations, name='participation'),
]