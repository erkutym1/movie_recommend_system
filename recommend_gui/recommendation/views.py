# your_app/views.py

from django.shortcuts import render

def index(request):
    return render(request, 'recommendation/index.html')  # 'index.html' dosyasını render edin


