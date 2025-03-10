from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Peraturan, KategoriPeraturan

class AdminBerkasPermissionMixin:
    """Mixin untuk membatasi akses hanya untuk superuser atau grup admin-berkas"""
    def has_module_permission(self, request):
        return request.user.is_superuser or request.user.groups.filter(name="admin-berkas").exists()

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.groups.filter(name="admin-berkas").exists()

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name="admin-berkas").exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name="admin-berkas").exists()

class PeraturanAdmin(AdminBerkasPermissionMixin, admin.ModelAdmin):
    list_display = ('nama_peraturan', 'nomor_peraturan', 'kategori_peraturan', 'status')
    search_fields = ('nama_peraturan',)
    list_filter = ('kategori_peraturan', 'status')

    # class Media:
    #     js = ("admin/js/dragdrop.js",)
    #     css = {"all": ("admin/css/dragdrop.css",)} 

class KategoriPeraturanAdmin(AdminBerkasPermissionMixin, admin.ModelAdmin):
    list_display = ('kode', 'nama')
    search_fields = ('nama',)

admin.site.register(KategoriPeraturan, KategoriPeraturanAdmin)
admin.site.register(Peraturan, PeraturanAdmin)
