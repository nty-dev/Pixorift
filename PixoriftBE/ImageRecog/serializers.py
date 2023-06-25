from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import TempImageUpload

User = get_user_model()

class ImageValidation(serializers.ModelSerializer):
    class Meta:
        model = TempImageUpload
        fields = ('player', 'imagefile')
