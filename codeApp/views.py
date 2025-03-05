from django.shortcuts import render, get_object_or_404
from .models import Peraturan, KategoriPeraturan
from .forms import PencarianForm


def dashboard(request):
    kategori_list = KategoriPeraturan.objects.all()
    jeda = {
        'title': "LHP Pondok Pesantren Nurul Jadid",
        'menu': 'dashboard',
        'kategori_list': kategori_list,
    }    
    return render(request, "dashboard.html", jeda)

def daftar_peraturan(request, kode_peraturan):
    kategori = get_object_or_404(KategoriPeraturan, kode=kode_peraturan.upper())
    peraturan_list = Peraturan.objects.filter(kategori_peraturan=kategori)
    jeda = {
        'title': kategori.nama,
        'menu': 'daftar_peraturan',
        'kategori': kategori,
        'peraturan_list': peraturan_list,
    }
    return render(request, 'peraturan_list.html', jeda)

def cari_peraturan(request):
    hasil = []
    query = ""

    if request.GET.get("query"):
        query = request.GET.get("query")
        hasil = Peraturan.objects.filter(teks_pdf__icontains=query)

    form = PencarianForm(initial={"query": query})
    return render(request, "cari_peraturan.html", {"form": form, "hasil": hasil})
