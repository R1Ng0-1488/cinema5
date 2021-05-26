from django.contrib import admin

from .models import AdvUser
# Register your models here.


@admin.register(AdvUser)
class AdvUserAdmin(admin.ModelAdmin):
	list_display = ['email', 'username']
	list_display_links = ['email', 'username']

