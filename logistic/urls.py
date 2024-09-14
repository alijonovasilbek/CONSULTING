from logistic import views
from django.urls import path


urlpatterns = [
    path('index/', views.index, name='index'),
    path('payments/',views.all_payments, name='all_payments'),
    path('todos/',views.all_todos,name='all_todos'),
    path('exhibitions/',views.all_exhibitions,name='all_exhibitions'),
    path('users/',views.all_users,name='all_users'),

]
