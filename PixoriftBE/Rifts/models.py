from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO
import sys
import os
# Create your models here.
User = get_user_model()

class Rift(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    content = models.CharField(max_length=1200, blank=True, null=True)
    upload_date = models.DateTimeField(default=timezone.now)
    edited = models.BooleanField(default=False)
    format = models.BooleanField(default=False)

    @property
    def images(self):
        return self.riftimage_set.all()

    @property
    def rating(self):
        return self.riftrating_set.filter(rating=True).count() - self.riftrating_set.filter(rating=False).count()

    class Meta:
        ordering = ('-upload_date',)

def RiftImagePath(instance, filename):
    return 'rifts/%s/%s/%s'%(instance.rift.author.id, instance.rift.id, 'a'+str(instance.rift.author.id)+'r'+str(instance.rift.id)+'.png')

class RiftImage(models.Model):
    rift = models.ForeignKey(Rift, on_delete=models.CASCADE, blank=False)
    image = models.ImageField(upload_to=RiftImagePath, null=True)

    def save(self, *args, **kwargs):
        tempim = Image.open(self.image)
        output = BytesIO()
        tempim.save(output, format='PNG')
        output.seek(0)
        aname = 'temp.png'
        image_path = self.image.path
        self.image = InMemoryUploadedFile(output, 'ImageField', aname, 'image/png', sys.getsizeof(output), None)
        if os.path.isfile(image_path):
        	os.remove(image_path)
        super(RiftImage, self).save(*args, **kwargs)

class RiftRating(models.Model):
    rater = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    rift = models.ForeignKey(Rift, on_delete=models.CASCADE, blank=False)
    rating = models.BooleanField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['rater', 'rating',], name='Rate-Once', )
        ]
