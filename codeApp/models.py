from django.db import models
import fitz  # PyMuPDF untuk ekstrak teks

class Peraturan(models.Model):
    STATUS_CHOICES = [
        ('berlaku', 'Berlaku'),
        ('tidak berlaku', 'Tidak Berlaku'),
    ]

  
    KATEGORI_CHOICES = [
        ('kdp', 'Keputusan Dewan Pengasuh & Pengasuh'),
        ('pkp', 'Peraturan Kepala Pesantren'),
        ('pbb', 'Peraturan Biro, Badan & Banom'),
        ('psp', 'Peraturan Satuan Pendidikan'),
        ('sop', 'Standard Operating Procedure'),
        ('kpp', 'Kompilasi Peraturan Pesantren'),
        ('kp', 'Keputusan Pimpinan'),
        ('rc', 'Rancangan Hukum'),
    ]



    nomor_peraturan = models.CharField(max_length=50, default='-')
    nama_peraturan = models.CharField(max_length=255)
    kategori_peraturan = models.CharField(max_length=50, choices=KATEGORI_CHOICES, default='rc')
    lembar_pesantren = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='berlaku')
    tahun = models.IntegerField(blank=True, null=True)
    kata_kunci = models.CharField(max_length=255, blank=True, null=True)
    file_pdf = models.FileField(upload_to="peraturan/")
    teks_pdf = models.TextField(blank=True, null=True)  # Simpan teks hasil ekstraksi
    created_at = models.DateTimeField(auto_now_add=True)
  

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Simpan file terlebih dahulu
        if self.file_pdf and not self.teks_pdf:
            self.teks_pdf = self.extract_text_from_pdf()
            super().save(update_fields=['teks_pdf'])  # Update hanya teks_pdf

    def extract_text_from_pdf(self):
        """Ekstrak teks dari file PDF tanpa menutup file terlalu cepat"""
        text = ""
        try:
            if self.file_pdf and hasattr(self.file_pdf, 'path'):  # Pastikan file ada
                with fitz.open(self.file_pdf.path) as doc:  # Baca langsung dari file path
                    text = "\n".join([page.get_text("text") for page in doc])
        except Exception as e:
            print(f"Error extracting text: {e}")
        return text.strip()  # Hapus spasi kosong

    def __str__(self):
        return self.nama_peraturan
    class Meta:
        verbose_name_plural = "Data Peraturan"
