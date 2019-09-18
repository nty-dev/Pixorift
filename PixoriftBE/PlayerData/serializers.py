from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *

User = get_user_model()

class PlayerLevelSerial(serializers.ModelSerializer):
    player = serializers.CharField(source='player.username')
    full_xp = serializers.IntegerField(source='fullxp', read_only=True)

    class Meta:
        model = PlayerData
        fields = ('player', 'level', 'xp', 'full_xp', 'totalxp')
