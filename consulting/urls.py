from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from passlib.handlers.django import django_disabled
from consulting import views


urlpatterns = [
    path('cons/', views.consulting, name='consulting')
]