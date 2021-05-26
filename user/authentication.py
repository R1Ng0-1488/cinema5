from django.contrib.auth import get_user_model

User = get_user_model()


class PhoneAuthentication:
	def authenticate(self, email, password):
		user = User.objects.get(email=email)
		if user.check_password(password):
			return user
		return None

	def get_user(self, email):
		try:
			return User.objects.get(email=email) 
		except User.DoesNotExist:
			return None