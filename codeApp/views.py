from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from .models import Peraturan, KategoriPeraturan, Kompilasi
from .forms import PencarianForm
from django.db.models import Q, Count
from django.contrib import messages
import json

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Username atau password salah")
    return render(request, 'login.html', {'title': 'Login LHP Pondok Pesantren Nurul Jadid'})

def dashboard(request):
    kategori_list = KategoriPeraturan.objects.all()
    
    # Filter berdasarkan hak akses user
    if request.user.is_authenticated and request.user.groups.filter(name='pegawai-pesantren').exists():
        peraturan_terbaru = Peraturan.objects.order_by('-created_at')[:5]
    else:
        peraturan_terbaru = Peraturan.objects.filter(hanya_untuk_pegawai=False).order_by('-created_at')[:5]


    jeda = {
        'title': "LHP Pondok Pesantren Nurul Jadid",
        'menu': 'dashboard',
        'kategori_list': kategori_list,
        'peraturan_terbaru': peraturan_terbaru,
    }    
    return render(request, "dashboard.html", jeda)


def latar_belakang(request):
    jeda = {
        'title': "Latar Belakang Lembaga Hukum Pondok Pesantren Nurul Jadid",
        'menu': 'profil-lembaga',
    }
    return render(request, "latar_belakang.html", jeda)

def visi_misi(request):
    jeda = {
        'title': "Visi Misi Lembaga Hukum Pondok Pesantren Nurul Jadid",
        'menu': 'profil-lembaga',
    }
    return render(request, "visi_misi.html", jeda)

def dasar_hukum(request):
    jeda = {
        'title': "Dasar Hukum LHP PP Nurul Jadid",
        'menu': 'profil-lembaga',
    }
    return render(request, 'dasar_hukum.html', jeda)

def organisasi(request):
    jeda = {
        'title': "Organisasi LHP PP Nurul Jadid",
        'menu': "profil-lembaga",
    }
    return render(request, "organisasi.html", jeda)

def mekanisme_regulasi(request):
    jeda = {
        'title': "Mekanisme dan Regulasi LHP PP Nurul Jadid",
        'menu': "profil-lembaga",
    }
    return render(request, "mekanisme.html", jeda)


def daftar_peraturan(request, kode_peraturan):
    kategori = get_object_or_404(KategoriPeraturan, kode=kode_peraturan.upper())

    # Filter berdasarkan hak akses user
    if request.user.is_authenticated and request.user.groups.filter(name='pegawai-pesantren').exists():
        peraturan_list = Peraturan.objects.filter(kategori_peraturan=kategori).order_by('-id')
    else:
        peraturan_list = Peraturan.objects.filter(kategori_peraturan=kategori, hanya_untuk_pegawai=False).order_by('-id')


    # Pagination
    paginator = Paginator(peraturan_list, 5)  # Tampilkan 5 per halaman
    page_number = request.GET.get('page')
    peraturan_list = paginator.get_page(page_number)

    # Rekapitulasi jumlah dokumen per kategori
    rekapitulasi = Peraturan.objects.values('kategori_peraturan__nama').annotate(jumlah=Count('id')).order_by('kategori_peraturan__nama')
    
    jeda = {
        'title': kategori.nama,
        'menu': 'kategori-peraturan',
        'kategori': kategori.nama,
        'peraturan_list': peraturan_list,
        'rekapitulasi': rekapitulasi,
    }
    return render(request, 'peraturan_list.html', jeda)


def kompilasi_peraturan(request):
    kompilasi_list = Kompilasi.objects.all()

    # Pagination
    paginator = Paginator(kompilasi_list, 5)  # Tampilkan 5 per halaman
    page_number = request.GET.get('page')
    kompilasi = paginator.get_page(page_number)
    
    jeda = {
        'title': "Kompilasi Peraturan Pondok Pesantren Nurul Jadid",
        'menu': 'kompilasi-peraturan',
        'kompilasi_list': kompilasi,
    }
    return render(request, "kompilasi_peraturan.html", jeda)


def daftar_peraturan_kompilasi(request, kompilasi):
    kompilasi = get_object_or_404(Kompilasi, slug=kompilasi)

    peraturan_list = Peraturan.objects.filter(kompilasi=kompilasi)

    # Pagination
    paginator = Paginator(peraturan_list, 5)  # Tampilkan 5 per halaman
    page_number = request.GET.get('page')
    peraturan_list = paginator.get_page(page_number)

    jeda = {
        'title': kompilasi.nama,
        'menu': 'kompilasi-peraturan',
        'kompilasi': kompilasi.nama,
        'peraturan_list': peraturan_list,
    }
    return render(request, 'peraturan_list_kompilasi.html', jeda)


def cari_peraturan(request):
    query = request.GET.get("q", "").strip()
    hasil = []

    if query:
        hasil = Peraturan.objects.filter(
            Q(nama_peraturan__icontains=query) |
            Q(teks_pdf__icontains=query)
        )[:5]  # Batasi hasil agar tidak berat

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = [
            {
                "nama_peraturan": peraturan.nama_peraturan,
                "teks_pdf": peraturan.teks_pdf[:100],  # Potong untuk tampilan singkat
                "view_url": peraturan.file_pdf.url,
                "download_url": peraturan.file_pdf.url,
            }
            for peraturan in hasil
        ]
        return JsonResponse({"results": data})

    return render(request, "dashboard.html")

