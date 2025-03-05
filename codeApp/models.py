from django.db import models
import fitz  # PyMuPDF untuk ekstraksi teks PDF

class KategoriPeraturan(models.Model):
    kode = models.CharField(max_length=10, unique=True)
    nama = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='icons/', null=True, blank=True)
    is_mobile_hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = "Kategori Peraturan"

class Peraturan(models.Model):
    STATUS_CHOICES = [
        ('berlaku', 'Berlaku'),
        ('tidak berlaku', 'Tidak Berlaku'),
    ]

    nomor_peraturan = models.CharField(max_length=50, default='-')
    nama_peraturan = models.CharField(max_length=255)
    kategori_peraturan = models.ForeignKey(KategoriPeraturan, on_delete=models.SET_NULL, null=True)
    lembar_pesantren = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='berlaku')
    tahun = models.IntegerField(blank=True, null=True)
    kata_kunci = models.CharField(max_length=255, blank=True, null=True)
    file_pdf = models.FileField(upload_to="peraturan/")
    teks_pdf = models.TextField(blank=True, null=True)  # Simpan teks hasil ekstraksi
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama_peraturan

    class Meta:
        verbose_name_plural = "Data Peraturan"


# SIGNAL UNTUK EKSTRAKSI TEKS PDF OTOMATIS
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Peraturan)
def extract_text_from_pdf(sender, instance, **kwargs):
    """Ekstrak teks PDF setelah peraturan disimpan"""
    if instance.file_pdf and not instance.teks_pdf:
        text = ""
        try:
            if hasattr(instance.file_pdf, 'path'):
                with fitz.open(instance.file_pdf.path) as doc:
                    text = "\n".join([page.get_text("text") for page in doc])
            instance.teks_pdf = text.strip()
            instance.save(update_fields=['teks_pdf'])  # Simpan teks_pdf saja
        except Exception as e:
            print(f"Error extracting text: {e}")
