from django.urls import path

from . import views


urlpatterns = [
    path('process/', views.PaymentProcess.as_view(), name='process'),
    path('done/<int:pk>', views.PaymentDone.as_view(), name='done'),
    path('canceled/', views.PaymentCanceled.as_view(), name='canceled'),
]