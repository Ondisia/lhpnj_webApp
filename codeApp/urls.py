from django.urls import path
from .views import cari_peraturan

urlpatterns = [
    path("", cari_peraturan, name="cari_peraturan"),
]
