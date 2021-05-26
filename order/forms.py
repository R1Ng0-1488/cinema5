from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from .models import Order


class OrderCreateForm(forms.ModelForm):
	# phone = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Номер телефона', 'class': 'form-input'}))
	email = forms.EmailField(label='', 
		widget=forms.TextInput(attrs={'placeholder': 'Электронная почта', 
													 'class': 'form-input',
													 'required': True}))
	
	class Meta:
		model = Order
		fields = ['email']
		error_messages = {'email': {'email': 'Введите корректный email'}}


class CustomUserCreationForm(UserCreationForm):

	class Meta:
		model = get_user_model()
		fields = ('email',)


class PhoneForm(forms.Form):
	email = forms.EmailField(label='',  widget=forms.EmailInput(
		attrs={'placeholder': 'Email', 'class': 'form-input'}))
	password = forms.CharField(label='', widget=forms.PasswordInput(
		attrs={'placeholder': 'Пароль', 'class': 'form-input'}))