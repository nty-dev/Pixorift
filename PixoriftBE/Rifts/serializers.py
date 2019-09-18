from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *
from datetime import *
import timeago
import pytz

User = get_user_model()

class URiftImageSerial(serializers.ModelSerializer):
    class Meta:
        model = RiftImage
        fields = ('image',)

class URiftSerial(serializers.ModelSerializer):
    images = URiftImageSerial(many=True)

    class Meta:
        model = Rift
        fields = ('author', 'content', 'images')

    def create(self, validated_data):
        imagemodel = validated_data.pop('images')
        riftpost = Rift.objects.create(**validated_data)
        for image in imagemodel:
            RiftImage.objects.create(rift=riftpost, **image)
        return riftpost

    def validate(self, data):
        if len(data['content']) == 0 and len(data['images']) == 0:
            raise serializers.ValidationError('You cannot submit a blank post!')
        return data

class DRiftImageSerial(serializers.ModelSerializer):
    class Meta:
        model = RiftImage
        fields = ('image',)

class DRiftSerial(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username')
    author_displayid = serializers.CharField(source='author.displayid')
    authoravatar = serializers.ImageField(source='author.useravatar')
    images = DRiftImageSerial(many=True, read_only=True)
    upload_date = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    def get_upload_date(self, dt):
        return timeago.format(dt.upload_date, datetime.utcnow().replace(tzinfo=pytz.utc))

    def get_rating(self, obj):
        return obj.riftrating_set.filter(rating=True).count() - obj.riftrating_set.filter(rating=False).count()

    class Meta:
        model = Rift
        fields = '__all__'

class RiftRatingSerial(serializers.ModelSerializer):
    class Meta:
        model = RiftRating
        fields = ('rater', 'rift', 'rating',)
