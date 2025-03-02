from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path("cari/", cari_peraturan, name="cari_peraturan"),
]
