from django.contrib import admin

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from movie.models import City
from .models import Share, PdfFiles
# Register your models here.


class CityInline(admin.TabularInline):
    model = City


class ShareAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())
    inlines = [CityInline]

    class Meta:
        model = Share
        fields = '__all__'


@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    form = ShareAdminForm
    prepopulated_fields = {'slug': ('title',)}


@admin.register(PdfFiles)
class PdfFilesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

