from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Peraturan, KategoriPeraturan
from .forms import PencarianForm
from django.db.models import Q, Count
import json


def dashboard(request):
    kategori_list = KategoriPeraturan.objects.all()

    peraturan_terbaru = Peraturan.objects.order_by('-created_at')[:5]

    jeda = {
        'title': "LHP Pondok Pesantren Nurul Jadid",
        'menu': 'dashboard',
        'kategori_list': kategori_list,
        'peraturan_terbaru': peraturan_terbaru,
    }    
    return render(request, "dashboard.html", jeda)


def profil_lembaga(request):
    jeda = {
        'title': "Profil Lembaga Hukum Pondok Pesantren Nurul Jadid",
        'menu': 'profil-lembaga',
    }
    return render(request, "profil_lembaga.html", jeda)


# def hubungi_lembaga(request):
#     jeda = {
#         'title': "Hubungi Lembaga Hukum Pondok Pesantren Nurul Jadid",
#         'menu': 'hubungi-lembaga',
#     }
#     return render(request, "hubungi_kami.html", jeda)

def daftar_peraturan(request, kode_peraturan):
    kategori = get_object_or_404(KategoriPeraturan, kode=kode_peraturan.upper())
    peraturan_list = Peraturan.objects.filter(kategori_peraturan=kategori)

    # Pagination
    paginator = Paginator(peraturan_list, 5)  # Tampilkan 5 per halaman
    page_number = request.GET.get('page')
    peraturan_list = paginator.get_page(page_number)

    # Rekapitulasi jumlah dokumen per kategori
    rekapitulasi = Peraturan.objects.values('kategori_peraturan__nama').annotate(jumlah=Count('id')).order_by('kategori_peraturan__nama')


    # Data untuk chart
    labels = json.dumps([r['kategori_peraturan__nama'] for r in rekapitulasi])
    data = json.dumps([r['jumlah'] for r in rekapitulasi])
    
    jeda = {
        'title': kategori.nama,
        'menu': 'kategori-peraturan',
        'kategori': kategori.nama,
        'peraturan_list': peraturan_list,
        'rekapitulasi': rekapitulasi,
        'chart_labels': labels,
        'chart_data': data,
    }
    return render(request, 'peraturan_list.html', jeda)


def cari_peraturan(request):
    query = request.GET.get("q", "").strip()
    hasil = []

    if query:
        # Versi SQLite (saat ini digunakan)
        hasil = Peraturan.objects.filter(
            Q(nama_peraturan__icontains=query) |
            Q(teks_pdf__icontains=query)
        )[:5]  # Batasi jumlah hasil untuk performa

        # Versi MySQL (aktifkan saat di production)
        # hasil = Peraturan.objects.annotate(
        #     relevansi=SearchRank(SearchVector('nama_peraturan', 'teks_pdf', 'kata_kunci'), SearchQuery(query))
        # ).filter(relevansi__gt=0).order_by('-relevansi')[:5]

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = [
            {
                "nama_peraturan": peraturan.nama_peraturan,
                "teks_pdf": peraturan.teks_pdf[:100],  # Potong teks agar tidak terlalu panjang
                "view_url": peraturan.file_pdf.url,
                "download_url": peraturan.file_pdf.url,
            }
            for peraturan in hasil
        ]
        return JsonResponse({"results": data})

    return render(request, "dashboard.html")

