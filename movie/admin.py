from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import (Movie, AgeLimit, Cinema, Session,
                     Hall, Place, Ticket, City, Row,
                     CinemaImages, SocialLinks, TitleQuestion,
                     Answer)


class AnswerAdminForm(forms.ModelForm):
    answer = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Answer
        fields = '__all__'


class AnswerInline(admin.TabularInline):
    model = Answer
    form = AnswerAdminForm


class CinemaImagesInline(admin.TabularInline):
    model = CinemaImages


class SocialLinks(admin.TabularInline):
    model = SocialLinks


class RowInline(admin.TabularInline):
    model = Row


class PlaceInline(admin.TabularInline):
    model = Place
    extra = 12


@admin.register(Row)
class RowAdmin(admin.ModelAdmin):
    inlines = [PlaceInline]
    

@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    inlines = [CinemaImagesInline]


@admin.register(TitleQuestion)
class TitleQuestionAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']
    inlines = [AnswerInline]


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    inlines = [RowInline]


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'duration_time')
    list_display_links = ('id', 'title')

    def duration_time(self, obj):
        return obj.duration.strftime("%H:%M:%S")


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    # inlines = [SocialLinks]
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(AgeLimit)
# admin.site.register(Cinema)
admin.site.register(Session)
# admin.site.register(Row)
# admin.site.register(Hall)
admin.site.register(Place)
admin.site.register(Ticket)
# admin.site.register(City)
