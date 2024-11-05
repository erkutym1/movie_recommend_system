# your_project/urls.py

from django.contrib import admin
from django.urls import path, include  # include'u ekleyin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recommendation.urls')),  # your_app uygulamasının URL'lerini ana URL'e dahil edin
]
