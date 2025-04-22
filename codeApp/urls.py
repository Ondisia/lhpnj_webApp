from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *

urlpatterns = [
    
    path('', dashboard, name="dashboard"),

    path('profil-lembaga-hukum-pondok-pesantren-nurul-jadid/', profil_lembaga, name='profil_lembaga'),

    path('kategori-peraturan/<str:kode_peraturan>/', daftar_peraturan, name='daftar_peraturan'),

    path("cari/", cari_peraturan, name="cari_peraturan"),

    path("kompilasi-peraturan-pesantren/", kompilasi_peraturan, name="kompilasi_peraturan"),

    # Login & Logout
    path("login/", login_user, name="login"),
    path("logout/", LogoutView.as_view(next_page='dashboard'), name="logout"),
    path('after-login/', after_login, name='after_login'),
]
