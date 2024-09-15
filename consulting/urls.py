from django.urls import path
from .views import consulting

urlpatterns = [
    path('consulting/', consulting, name='consulting'),
]
