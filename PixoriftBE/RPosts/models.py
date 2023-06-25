from django.db import models
from django.contrib.auth import get_user_model
from datetime import *
from django.utils import timezone
# Create your models here.
User = get_user_model()

class ImageDataBank(models.Model):
    imagefile = models.ImageField(upload_to='Posts/')

class PixoPost(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    images = models.ManyToManyField(ImageDataBank, blank=True)
    title = models.CharField(max_length=100, blank=False)
    text = models.CharField(max_length=10000, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
