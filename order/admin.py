from django.contrib import admin

from .models import Order
from movie.models import Ticket
# Register your models here.


class TicketInline(admin.TabularInline):
    model = Ticket
    raw_id_fields = ['place', 'session']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'paid', 'created', 'updated')
    list_filter = ('paid', 'created', 'updated')
    inlines = (TicketInline,)