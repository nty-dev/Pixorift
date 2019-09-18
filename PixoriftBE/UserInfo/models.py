# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO
import sys
import os

avatar_dir = 'avatars/'

genders = [
	('M', 'Male'),
	('F', 'Female'),
	('None', 'Genderless')
]

class Account(AbstractUser):
		username = models.CharField(max_length=16, unique=True)
		displayid = models.CharField(max_length=20)
		userbio = models.CharField(max_length=200, blank=True)
		email = models.EmailField(blank=False, unique=True)
		useravatar = models.ImageField(upload_to=avatar_dir, blank=True, default='%sblank.png'%avatar_dir)
		birth_date = models.DateField(null=True, blank=True)
		gender = models.CharField(null=True, choices=genders, max_length=1)
		privated = models.BooleanField(default=False)
		email_verified = models.BooleanField(default=False)

		USERNAME_FIELD = 'username'
		EMAIL_FIELD = 'email'
		REQUIRED_FIELDS = ['displayid', 'email']

		def save(self, *args, **kwargs):
			if self.useravatar.name != '%sblank.png'%avatar_dir and self.id != None:
				tempim = Image.open(self.useravatar)
				output = BytesIO()
				width, height = tempim.size
				if width == height:
					pass
				elif width > height:
					tempim = tempim.crop((0, 0, height, height))
				elif height > width:
					tempim = tempim.crop((0, 0, width, width))
				tempim = tempim.resize((800, 800))
				tempim.save(output, format='PNG')
				output.seek(0)
				aname = '%spfp.png'%str(self.id)
				avatar_path = self.useravatar.path
				self.useravatar = InMemoryUploadedFile(output, 'ImageField', aname, 'image/png', sys.getsizeof(output), None)
				if os.path.isfile(avatar_path):
					os.remove(avatar_path)
			super(Account, self).save(*args, **kwargs)
