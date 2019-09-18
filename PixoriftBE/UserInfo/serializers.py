from django.contrib.auth import get_user_model
from rest_framework import serializers
from PixoUM.models import *
from Rifts.models import *
from PlayerData.models import *

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
	followers = serializers.SerializerMethodField()
	following = serializers.SerializerMethodField()
	riftcount = serializers.SerializerMethodField()
	level = serializers.SerializerMethodField()
	xp = serializers.SerializerMethodField()
	fullxp = serializers.SerializerMethodField()
	gender = serializers.SerializerMethodField()

	def get_fullxp(self, o):
		return o.playerdata_set.fullxp()

	def get_level(self, o):
		return o.playerdata_set.level

	def get_xp(self, o):
		return o.playerdata_set.xp

	def get_riftcount(self, o):
		return o.rift_set.count()

	def get_followers(self, o):
		return o.following.count()

	def get_following(self, o):
		return o.followers.count()

	def get_gender(self, o):
		return o.get_gender_display()

	class Meta:
		model = get_user_model()
		fields =  (
			'id',
			'displayid',
			'last_login',
			'is_superuser',
			'first_name',
			'last_name',
			'date_joined',
			'username',
			'userbio',
			'email',
			'useravatar',
			'birth_date',
			'groups',
			'user_permissions',
			'followers',
			'following',
			'riftcount',
			'level',
			'xp',
			'fullxp',
			'gender',
			'privated'
		)

class PublicUserSerializer(serializers.ModelSerializer):
	followers = serializers.SerializerMethodField()
	following = serializers.SerializerMethodField()
	riftcount = serializers.SerializerMethodField()
	level = serializers.SerializerMethodField()
	xp = serializers.SerializerMethodField()
	fullxp = serializers.SerializerMethodField()
	gender = serializers.SerializerMethodField()

	def get_fullxp(self, o):
		return PlayerData.objects.get(player=o).fullxp()

	def get_level(self, o):
		return PlayerData.objects.get(player=o).level

	def get_xp(self, o):
		return PlayerData.objects.get(player=o).xp

	def get_riftcount(self, o):
		return o.rift_set.count()

	def get_followers(self, o):
		return o.following.count()

	def get_following(self, o):
		return o.followers.count()

	def get_gender(self, o):
		return o.get_gender_display()

	class Meta:
		model = get_user_model()
		fields =  (
			'id',
			'username',
			'displayid',
			'userbio',
			'useravatar',
			'followers',
			'following',
			'riftcount',
			'level',
			'xp',
			'fullxp',
			'gender',
			'privated',
			'email_verified'
		)

class UserCreation(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ('username', 'displayid', 'first_name', 'last_name', 'userbio', 'email', 'useravatar', 'gender', 'birth_date', 'password')

	def create(self, vd, *args, **kwargs):
		user = super(UserCreation, self).create(vd, *args, **kwargs)
		user.set_password(vd['password'])
		user.save()
		return user

class UpdateUserSerial(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'displayid', 'first_name', 'last_name', 'userbio', 'email', 'useravatar', 'gender', 'birth_date')
