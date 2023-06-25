from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = get_user_model()
		fields = (
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
			'user_permissions'
		)

class PublicUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = get_user_model()
		fields = (
			'username',
			'displayid',
			'userbio',
			'useravatar'
		)

class UserCreation(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ('username', 'displayid', 'first_name', 'last_name', 'userbio', 'email', 'useravatar', 'birth_date', 'password')

	def create(self, vd):
		user = super(UserCreation, self).create(vd)
		user.set_password(vd['password'])
		user.save()
		return user

class UpdateUserSerial(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'displayid', 'first_name', 'last_name', 'userbio', 'email', 'useravatar', 'birth_date')
