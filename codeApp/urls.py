from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('kategori-peraturan/<str:kode_peraturan>/', daftar_peraturan, name='daftar_peraturan'),
    path("cari/", cari_peraturan, name="cari_peraturan"),
]
