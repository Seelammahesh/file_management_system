from django.contrib import admin
from .models import Folder, File


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'owner', 'created_at', 'file_count')
    list_filter = ('created_at', 'owner')
    search_fields = ('name', 'owner__username')
    readonly_fields = ('created_at', 'updated_at')
    
    def file_count(self, obj):
        return obj.files.count()
    file_count.short_description = 'Files'


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'owner', 'folder', 'file_size_display', 'uploaded_at')
    list_filter = ('uploaded_at', 'owner', 'folder')
    search_fields = ('name', 'owner__username', 'folder__name')
    readonly_fields = ('file_size', 'uploaded_at')
    
    def file_size_display(self, obj):
        size_mb = obj.file_size / (1024 * 1024)
        return f"{size_mb:.2f} MB"
    file_size_display.short_description = 'Size'