from django.urls import path
from django.contrib.auth.views import (LogoutView, 
	PasswordResetView, PasswordResetConfirmView,
	PasswordResetDoneView, PasswordResetCompleteView)

from . import views
from .forms import AdvPasswordResetForm, AdvPasswordChangeForm

urlpatterns = [
	path('check', views.CheckPhone.as_view(), name='check_phone'),
	path('use_bonuses/', views.CreateUserOrderView.as_view(), name='use_bonuses'),
	path('check_email/', views.CheckEmail.as_view(), name='check_email'),
	path('acoount/', views.Account.as_view(), name='account'),
	path('account/logout', LogoutView.as_view(), name='logout'),
	path('account/password_reset', PasswordResetView.as_view(
		template_name='user/password_reset.html',
		email_template_name='user/password_reset_email.html',
		form_class=AdvPasswordResetForm
		), name='password_reset'),
	path('account/password_reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
		template_name='user/password_reset_confirm.html',
		form_class=AdvPasswordChangeForm), name='password_reset_confirm'),
	path('account/password_reset/done', PasswordResetDoneView.as_view(
		template_name='user/password_reset_done.html'), name='password_reset_done'),
	path('account/password_reset/complete', PasswordResetCompleteView.as_view(
		template_name='user/password_reset_complete.html'
		), name='password_reset_complete'),
	path('account/update_user/<int:pk>/', views.UpdateAccountView.as_view(), name='update_user'),
]