from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model, authenticate
from .serializers import *
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .tauth import tauth
from django.core.files.storage import FileSystemStorage

User = get_user_model()

class usernameavail(APIView):
	def get(self, request):
		usernamecheck = self.request.GET.get('username_req')
		if User.objects.filter(username=usernamecheck).exists():
			return Response({'check': 'False'})
		else:
			return Response({'check': 'True'})

class publicusercall(APIView):
	def get(self, request):
		specuser = self.request.GET.get('username_req')
		if specuser == "ALL":
			return Response(PublicUserSerializer(User.objects.all(), many=True).data)
		userlist = User.objects.filter(username=specuser)
		serializer = PublicUserSerializer(userlist, many=True)
		return Response(serializer.data)

class privateusercall(APIView):
	def get(self, request):
		vtoken = self.request.GET.get('Auth')
		username = self.request.GET.get('username')
		if not tauth(vtoken, username)['status']:
			return tauth(vtoken, username)['response']
		serializer = UserSerializer([tauth(vtoken, username)['response']], many=True)
		return Response(serializer.data[0])

class create_account(APIView):
	def post(self, request):
		usersignup = UserCreation(data=self.request.data)
		if usersignup.is_valid():
			usersignup.save()
			username = request.data.get('username')
			password = request.data.get('password')
			UserLogin = authenticate(username=username, password=password)
			PlayerData.objects.create(player=UserLogin)
			logintoken = Token.objects.create(user=UserLogin)
			return Response({'token': logintoken.key, 'state': 'Success'}, status=status.HTTP_200_OK)
		return Response({'errors': usersignup.errors, 'state': 'Denied'}, status=status.HTTP_400_BAD_REQUEST)

class change_account(APIView):
	def post(self, request):
		vtoken = self.request.data.get('Auth')
		username = self.request.data.get('oldusername')
		if not tauth(vtoken, username)['status']:
			return tauth(vtoken, username)['response']
		current_user = tauth(vtoken, username)['response']
		updaterequest = self.request.data
		userupdate = UpdateUserSerial(data=updaterequest, instance=current_user)
		if userupdate.is_valid():
			userupdate.save()
			serializer = UserSerializer([User.objects.get(username=self.request.data.get('username'))], many=True)
			return Response({'state': 'Success', 'update': serializer.data}, status=status.HTTP_200_OK)
		return Response({'errors': userupdate.errors, 'state': 'Denied'}, status=status.HTTP_400_BAD_REQUEST)

class delete_account(APIView):
	def post(self, request):
		vtoken = self.request.data.get('Auth')
		username = self.request.data.get('username')
		password = self.request.data.get('password')
		UserVerify = authenticate(username=username, password=password)
		if not UserVerify:
			return Response({'error': 'Invalid login details. Account refuses to be deleted.', 'state': 'Denied'}, status=status.HTTP_401_UNAUTHORIZED)
		if not tauth(vtoken, UserVerify.username)['status']:
			return Response({'error': 'Invalid login token! Account refuses to be deleted.', 'state': 'Denied'}, status=status.HTTP_401_UNAUTHORIZED)
		UserVerify.delete()
		return Response({'state': 'Success'})

class change_password(APIView):
	def post(self, request):
		vtoken = self.request.data.get('Auth')
		username = self.request.data.get('username')
		oldpassword = self.request.data.get('oldpassword')
		password1 = self.request.data.get('password1')
		password2 = self.request.data.get('password2')
		UserVerify = authenticate(username=username, password=oldpassword)
		if not UserVerify:
			return Response({'error': 'Invalid login details. Password cannot be changed.', 'state': 'Denied'}, status=status.HTTP_401_UNAUTHORIZED)
		if not tauth(vtoken, UserVerify.username)['status']:
			return Response({'error': 'Invalid login token! Password cannot be changed!', 'state': 'Denied'}, status=status.HTTP_401_UNAUTHORIZED)
		if password1 != password2:
			return Response({'error': 'Password and Confirm Password have different values! Please re-enter your password!', 'state': 'Denied'}, status=status.HTTP_400_BAD_REQUEST)
		UserVerify.set_password(password1)
		UserVerify.save()
		return Response({'message': 'Password changed successfully!', 'state': 'Success'}, status=status.HTTP_200_OK)

class logout(APIView):
	def get(self, request):
		stoken = self.request.GET.get("Auth")
		if not Token.objects.filter(key=stoken).exists():
			return Response({'error': 'No user logged in with this token!', 'state': 'Denied'}, status=status.HTTP_400_BAD_REQUEST)
		logoutuser = Token.objects.get(key=stoken).user
		Token.objects.get(key=stoken).delete()
		return Response({'user': logoutuser.username, 'state': 'Success'})

class logincall(APIView):
	def post(self, request):
		username = self.request.data.get('username')
		password = self.request.data.get('password')
		if username is None or password is None or username == '' or password == '':
			return Response(
				{
				'error': 'Please enter both a Username and Password!',
				'state': 'Denied'
				},
				status = status.HTTP_400_BAD_REQUEST
			)
		UserLogin = authenticate(username=username, password=password)
		if not UserLogin:
			return Response(
				{
				'error': 'Your Username or Password is invalid!',
				'state': 'Denied'
				},
				status = status.HTTP_401_UNAUTHORIZED
			)
		if Token.objects.filter(user=UserLogin).exists():
			Token.objects.filter(user=UserLogin).delete()
		usertoken = Token.objects.create(user=UserLogin)
		return Response({'token': usertoken.key, 'state': 'Success'}, status=status.HTTP_200_OK)
