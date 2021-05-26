from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
from django import forms


class RegisterForm(UserCreationForm):

	class Meta:
		model = get_user_model()
		fields = ('username', 'password1', 'password2')


class LoginForm(AuthenticationForm):

	class Meta:
		model = get_user_model()
		fields = ('email', 'password')


class AdvUserUpdateForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		instance = getattr(self, 'instance', None)
		self.fields['email'].widget.attrs['class'] = 'form-input'
		self.fields['first_name'].widget.attrs['class'] = 'form-input'
		self.fields['last_name'].widget.attrs['class'] = 'form-input'
		self.fields['first_name'].widget.attrs['placeholder'] = 'Имя'
		self.fields['last_name'].widget.attrs['placeholder'] = 'Фамилие'
		if instance and instance.pk:
			self.fields['email'].widget.attrs['readonly'] = True


	class Meta:
		model = get_user_model()
		fields = ('first_name', 'last_name', 'email')

	def clean_email(self):
		instance = getattr(self, 'instance', None)
		if instance and instance.pk:
			return instance.email
		else:
			return self.cleaned_data['email']


class AdvPasswordResetForm(PasswordResetForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['email'].widget.attrs['class'] = 'form-input'
		self.fields['email'].widget.attrs['placeholder'] = 'email'

class AdvPasswordChangeForm(SetPasswordForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		print('aaaaaaaaaaa', self.fields)
		self.fields['new_password1'].widget.attrs['class'] = 'form-input'
		self.fields['new_password2'].widget.attrs['class'] = 'form-input'
		self.fields['new_password1'].widget.attrs['placeholder'] = 'Введите пароль'
		self.fields['new_password2'].widget.attrs['placeholder'] = 'Введите пароль еще раз'