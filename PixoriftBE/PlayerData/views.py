from django.shortcuts import render
from django.core.files.storage import FileSystemStorage, Storage
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from UserInfo.tauth import tauth
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model, authenticate
from django.core import serializers
from .serializers import *
from .models import *
# Create your views here.

User = get_user_model()

class Get_Level(APIView):
    def post(self, request):
        username = self.request.data.get('username')
        vtoken = self.request.data.get('Auth')
        if not tauth(vtoken, username)['status']:
            return tauth(vtoken, username)['response']
        current_user = tauth(vtoken, username)['response']
        if not PlayerData.objects.filter(player=current_user).exists():
            PlayerData.objects.create(player=current_user)
        res = PlayerLevelSerial([PlayerData.objects.get(player=current_user)], many=True).data[0]
        return Response({'state':'Success', 'data':res}, status=status.HTTP_200_OK)

class EditLevel(APIView):
    def post(self, request):
        username = self.request.data.get('username')
        vtoken = self.request.data.get('Auth')
        if not tauth(vtoken, username)['status']:
            return tauth(vtoken, username)['response']
        current_user = tauth(vtoken, username)['response']
        if not current_user.is_superuser:
            return Response({'state': 'Denied', 'reason': 'You are not a superuser!'}, status=status.HTTP_401_UNAUTHORIZED)
        changeuser = self.request.data.get('changeusername')
        amount = self.request.data.get('amount')
        if type(amount) != int:
            try:
                amount = int(amount)
            except:
                return Response({'state': 'Denied', 'reason': 'Amount is not integer.'}, status=status.HTTP_400_BAD_REQUEST)
        if changeuser == None:
            changeuser = current_user
        elif not User.objects.filter(username=changeuser).exists():
            return Response({'state': 'Denied', 'reason': 'User does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            changeuser = User.objects.get(username=changeuser)
        editlvl = self.request.data.get('editlvl')
        if editlvl == 't':
            editlevel = True
        elif editlvl == 'f':
            editlevel = False
        else:
            editlevel = bool(editlvl)
        if not PlayerData.objects.filter(player=changeuser).exists():
            PlayerData.objects.create(player=changeuser)
        if editlevel:
            PlayerData.objects.get(player=changeuser).level_edit(amount)
        else:
            PlayerData.objects.get(player=changeuser).xp_edit(amount)
        res = PlayerLevelSerial([PlayerData.objects.get(player=changeuser)], many=True).data[0]
        return Response({'state':'Success', 'data':res}, status=status.HTTP_200_OK)
