from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *
import humanize

User = get_user_model()

class RPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PixoPost
        exclude = ('date_posted')

class RPostRetrieve(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username')

    def get_date_posted(self, dt):
        return 'Posted ' + humanize(dt.date_posted)

    class Meta:
        model = PixoPost
        fields = '__all__'
