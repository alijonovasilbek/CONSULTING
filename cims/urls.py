
from django.contrib import admin
from django.urls import path, include
from  django.conf.urls.static import static
from passlib.handlers.django import django_disabled

from django.conf import settings

urlpatterns = [
    path('ceo/', admin.site.urls),
    path('',include('main.urls')),
    path('',include('logistic.urls')),
    path('',include('telegram.urls')),
    path('', include('consulting.urls')),
    path('c/', include('ceo.urls')),
    path('',include('service.urls'))
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
