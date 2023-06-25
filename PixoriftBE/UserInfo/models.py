# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import FileSystemStorage

class Account(AbstractUser):
		username = models.CharField(max_length=16, unique=True)
		displayid = models.CharField(max_length=20)
		userbio = models.CharField(max_length=200, blank=True)
		email = models.EmailField(blank=False, unique=True)
		useravatar = models.ImageField(upload_to='avatars/', blank=True, default='avatars/noimg.jpg')
		birth_date = models.DateField(null=True, blank=True)

		USERNAME_FIELD = 'username'
		EMAIL_FIELD = 'email'
		REQUIRED_FIELDS = ['displayid', 'email']
