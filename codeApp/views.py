from django.shortcuts import render
from .models import Peraturan
from .forms import PencarianForm

def cari_peraturan(request):
    hasil = []
    query = ""

    if request.GET.get("query"):
        query = request.GET.get("query")
        hasil = Peraturan.objects.filter(teks_pdf__icontains=query)

    form = PencarianForm(initial={"query": query})
    return render(request, "cari_peraturan.html", {"form": form, "hasil": hasil})
