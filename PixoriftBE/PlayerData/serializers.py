from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *

User = get_user_model()

class PlayerDataSerial(serializers.ModelSerializer):
    player = serializers.CharField(source='player.username')
    full_xp = serializers.CharField(default=1000)

    class Meta:
        model = PlayerData
        fields = '__all__'
