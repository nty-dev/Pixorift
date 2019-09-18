from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *

User = get_user_model()

class FollowSerial(serializers.ModelSerializer):

    def validate(self, data):
        if data['follower'] == data['following']:
            raise serializers.ValidationError({'Self-Follow': 'You cannot follow yourself!'})
        return data

    class Meta:
        model = Follow
        fields = ('follower', 'following',)

class RFollowSerial(serializers.ModelSerializer):
    follower = serializers.CharField(source='follower.username')
    following = serializers.CharField(source='following.username')

    class Meta:
        model = Follow
        fields = ('follower', 'following',)
