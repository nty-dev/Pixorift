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

class PlayerDataInfo(APIView):
    def get(self, request):
        username = self.request.GET.get('username')
        vtoken = self.request.GET.get('Auth')
        if not tauth(vtoken, username)['status']:
            return tauth(vtoken, username)['response']
        current_user = tauth(vtoken, username)['response']
        if PlayerData.objects.filter(player=current_user).exists():
            PDobj = PlayerData.objects.get(player=current_user)
            return Response({'state': 'Success', 'Level': PDobj.level, 'XP': PDobj.xp, 'full_xp': 1000})
        else:
            PlayerData.objects.create(player=current_user)
            PDobj = PlayerData.objects.get(player=current_user)
            return Response({'state': 'Success', 'Level': PDobj.level, 'XP': PDobj.xp, 'full_xp': 1000})

@method_decorator(cache_page(60), name='dispatch')
class PlayerDataLB(APIView):
    def get(self, request):
        PDQuery = PlayerData.objects.order_by('level', 'xp').reverse()[:20]
        PDinfo = PlayerDataSerial(PDQuery, many=True).data
        runno = 1
        for i in PDinfo:
            i['position'] = runno
            runno = runno +1
        return Response({'info': PDinfo})

class AdminPDAddition(APIView):
    def get(self, request):
        username = self.request.GET.get('username')
        vtoken = self.request.GET.get('Auth')
        amount = self.request.GET.get('amount')
        editusername = self.request.GET.get('editusername')
        try:
            amount = int(amount)
        except:
            return Response({'state': 'Denied', 'Error': 'Amount is not integer.'}, status=status.HTTP_400_BAD_REQUEST)
        if not tauth(vtoken, username)['status']:
            return tauth(vtoken, username)['response']
        current_user = tauth(vtoken, username)['response']
        if editusername == None or not User.objects.filter(username=editusername).exists():
            editusername = current_user.username
        edituser = User.objects.get(username=editusername)
        if current_user.is_superuser:
            if PlayerData.objects.filter(player=edituser).exists():
                PDobj = PlayerData.objects.get(player=edituser)
            else:
                PlayerData.objects.create(player=edituser)
                PDobj = PlayerData.objects.get(player=edituser)
            PDobj.xp_gain(amount)
            return Response({'state': 'Success', 'username': editusername, 'Level': PDobj.level, 'XP': PDobj.xp})
        else:
            return Response({'state': 'Denied', 'Error': 'You do not have permissions to use this command!'}, status=status.HTTP_401_UNAUTHORIZED)

class Test(APIView):
    def post(self, request):
        print(self.request.data['test'])
        image_test = self.request.data.get('images')
        b = 0
        for i in image_test:
            b = b + 1
        print(b)
        t = self.request.data
        t['images'] = None
        return Response(self.request.data)
