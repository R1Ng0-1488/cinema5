from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator, EmailValidator
# Create your models here.


class UserAccountManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		if not email:
			raise ValueError('Email address must be provided')

		if not password:
			raise ValueError('Password must be provided')

		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email=None, password=None, **extra_fields):
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		extra_fields['is_staff'] = True
		extra_fields['is_superuser'] = True
		return self._create_user(email, password, **extra_fields)
 

class AdvUser(AbstractUser):

	objects = UserAccountManager()

	# phone = models.CharField(max_length=11, default='', unique=True)
	email = models.EmailField('email', unique=True, blank=False, null=False,
		validators=[EmailValidator()])
	username = models.CharField(max_length=35, blank=True, null=True, default='')
	bonuses = models.IntegerField(default=0, validators=[MinValueValidator(0)])
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
