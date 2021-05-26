from django.urls import path

from . import views

urlpatterns = [
    path('create', views.CreateOrderView.as_view(), name='order_create'),
    path('cancel_tickets', views.CancelTickets.as_view(), name='cancel_tickets'),
]