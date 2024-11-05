# your_app/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views  # views dosyasını içe aktarın

urlpatterns = [
    path('', views.index, name='index'),  # Anasayfa olarak 'index' görünümünü yönlendirin
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
