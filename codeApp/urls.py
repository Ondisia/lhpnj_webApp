from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.dashboard, name='dashboard'),

    path('latar-belakang-lhpnj/', views.latar_belakang, name='profil_latar_belakang'),
    path('visi-misi-lhpnj/', views.visi_misi, name='profil_visi_misi'),
    path('dasar-hukum-lhpnj/', views.dasar_hukum, name='profil_dasar_hukum'),

    path('kategori-peraturan/<str:kode_peraturan>/', views.daftar_peraturan, name='daftar_peraturan'),

    path('cari/', views.cari_peraturan, name='cari_peraturan'),

    path('kompilasi-peraturan-pesantren/', views.kompilasi_peraturan, name='kompilasi_peraturan'),

    path('daftar-peraturan-<str:kompilasi>/', views.daftar_peraturan_kompilasi, name='daftar_peraturan_kompilasi'),

    # Login & Logout
    path('login/', views.login_user, name='login'),
    path('logout/', LogoutView.as_view(next_page='dashboard'), name='logout'),
]
