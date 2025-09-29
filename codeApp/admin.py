from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Peraturan, KategoriPeraturan, Kompilasi, KategoriAccessUser, RancanganPeraturan

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


class PeraturanAdmin(admin.ModelAdmin):
    list_display = ('nama_peraturan', 'nomor_peraturan', 'kategori_peraturan', 'status')
    search_fields = ('nama_peraturan',)
    list_filter = ('kategori_peraturan', 'status')

    def has_module_permission(self, request):
        # Hanya tampilkan menu ini untuk superuser atau anggota grup admin-berkas
        return request.user.is_superuser or request.user.groups.filter(name="admin-berkas").exists()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "kategori_peraturan" and not request.user.is_superuser:
            allowed_kategori_ids = KategoriAccessUser.objects.filter(user=request.user).values_list('kategori_id', flat=True)
            kwargs["queryset"] = KategoriPeraturan.objects.filter(id__in=allowed_kategori_ids)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return KategoriAccessUser.objects.filter(user=request.user).exists()


class KategoriPeraturanAdmin(AdminBerkasPermissionMixin, admin.ModelAdmin):
    list_display = ('kode', 'nama')
    search_fields = ('nama',)

    def has_module_permission(self, request):
        # Hanya tampilkan menu ini untuk superuser
        return request.user.is_superuser


class KompilasiAdmin(AdminBerkasPermissionMixin, admin.ModelAdmin):
    list_display = ('nama', 'deskripsi')
    search_fields = ('nama',)
    list_filter = ('nama',)

    def has_module_permission(self, request):
        # Hanya tampilkan menu ini untuk superuser
        return request.user.is_superuser


class KategoriAccessUserAdmin(AdminBerkasPermissionMixin, admin.ModelAdmin):
    list_display = ('user', 'kategori')
    list_filter = ('kategori',)
    search_fields = ('user__username', 'kategori__nama')

    def has_module_permission(self, request):
        # Hanya tampilkan menu ini untuk superuser
        return request.user.is_superuser

class RancanganPeraturanAdmin(admin.ModelAdmin):
    list_display = ("nama_rancangan", "pengusul", "kategori_peraturan", "status", "created_at")
    list_filter = ("status", "kategori_peraturan")
    search_fields = ("nama_rancangan", "pengusul__username")
    readonly_fields = ("pengusul", "created_at", "updated_at")

    def save_model(self, request, obj, form, change):
        # otomatis set pengusul jika user biasa yang tambah
        if not obj.pk and not request.user.is_superuser and not request.user.groups.filter(name="admin-berkas").exists():
            obj.pengusul = request.user
        super().save_model(request, obj, form, change)

    def has_module_permission(self, request):
        # Semua user bisa mengajukan (tampil di menu), tapi hak akses beda
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.groups.filter(name="admin-berkas").exists():
            return True  # admin LHP bisa ubah status
        if obj and obj.pengusul == request.user and obj.status == "draft":
            return True  # user hanya bisa edit draft mereka sendiri
        return False



admin.site.register(Peraturan, PeraturanAdmin)
admin.site.register(KategoriPeraturan, KategoriPeraturanAdmin)
admin.site.register(Kompilasi, KompilasiAdmin)
admin.site.register(KategoriAccessUser, KategoriAccessUserAdmin)
admin.site.register(RancanganPeraturan, RancanganPeraturanAdmin)
