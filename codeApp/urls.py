from django.urls import path
from .views import *

urlpatterns = [
    
    path('', dashboard, name="dashboard"),

    path('profil-lembaga-hukum-pondok-pesantren-nurul-jadid/', profil_lembaga, name='profil_lembaga'),

    path('kategori-peraturan/<str:kode_peraturan>/', daftar_peraturan, name='daftar_peraturan'),

    # path('hubungi-lembaga-hukum-pondok-pesantren-nurul-jadid/', hubungi_lembaga, name='hubungi_lembaga'),

    path("cari/", cari_peraturan, name="cari_peraturan"),
]
