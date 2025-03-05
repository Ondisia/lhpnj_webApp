from django.contrib import admin
from .models import Peraturan, KategoriPeraturan

class PeraturanAdmin(admin.ModelAdmin):
    list_display = ('nama_peraturan', 'created_at')
    search_fields = ('nama_peraturan',)

    def has_module_permission(self, request):
        """Izinkan akses hanya untuk grup tertentu"""
        return request.user.is_superuser or request.user.groups.filter(name="admin-berkas").exists()

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.groups.filter(name="admin-berkas").exists()

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name="admin-berkas").exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name="admin-berkas").exists()

class KategoriPeraturanAdmin(admin.ModelAdmin):
    list_display = ('kode', 'nama')
    search_fields = ('nama',)

    def has_module_permission(self, request):
        """Izinkan akses hanya untuk grup tertentu"""
        return request.user.is_superuser or request.user.groups.filter(name="admin-berkas").exists()

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.groups.filter(name="admin-berkas").exists()

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name="admin-berkas").exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name="admin-berkas").exists()

admin.site.register(KategoriPeraturan)
admin.site.register(Peraturan, PeraturanAdmin)