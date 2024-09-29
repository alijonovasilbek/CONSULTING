from django.urls import path
from service import views

urlpatterns = [

    path('serviceall/',views.service_all, name='service_all'),
    path('service-users/',views.service_users, name='service_users'),
    path('service-messages/',views.service_messages, name='service_messages'),
    path('service-profiles/',views.service_profiles, name='service_profiles'),
    path('service-referrals/',views.service_referrals, name='service_referrals'),
    path('service-referreds/',views.service_referreds, name='service_referreds'),
]