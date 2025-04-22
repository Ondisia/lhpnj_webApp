from django.db import models
import fitz  # PyMuPDF

class KategoriPeraturan(models.Model):
    kode = models.CharField(max_length=10, unique=True)
    nama = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='icons/', null=True, blank=True)
    is_mobile_hidden = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nama} ({self.kode})"
    
    class Meta:
        verbose_name_plural = "Kategori Peraturan"

class Kompilasi(models.Model):
    nama = models.CharField(max_length=255, unique=True)
    deskripsi = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = "Kompilasi Peraturan"

class Peraturan(models.Model):
    STATUS_CHOICES = [
        ('berlaku', 'Berlaku'),
        ('tidak berlaku', 'Tidak Berlaku'),
    ]

    nomor_peraturan = models.CharField(max_length=50, default='-')
    nama_peraturan = models.CharField(max_length=255)
    kategori_peraturan = models.ForeignKey(KategoriPeraturan, on_delete=models.SET_NULL, null=True, blank=True)
    kompilasi = models.ForeignKey(Kompilasi, on_delete=models.SET_NULL, null=True, blank=True)
    hanya_untuk_pegawai = models.BooleanField(default=False, help_text="Centang jika peraturan hanya untuk pegawai pesantren")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='berlaku')
    tahun = models.IntegerField(blank=True, null=True)
    file_abstract = models.FileField(upload_to="abstracts/", blank=True, null=True)
    file_pdf = models.FileField(upload_to="peraturan/")
    teks_pdf = models.TextField(blank=True, null=True)
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
    if instance.file_abstract and not instance.teks_pdf:
        text = ""
        try:
            if hasattr(instance.file_abstract, 'path'):
                with fitz.open(instance.file_abstract.path) as doc:
                    text = "\n".join([page.get_text("text") for page in doc])
            instance.teks_pdf = text.strip()
            instance.save(update_fields=['teks_pdf'])
        except Exception as e:
            print(f"Error extracting text: {e}")
