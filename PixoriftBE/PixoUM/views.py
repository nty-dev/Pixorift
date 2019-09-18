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

class FollowView(APIView):
    def post(self, response):
        username = self.request.data.get('username')
        vtoken = self.request.data.get('Auth')
        if not tauth(vtoken, username)['status']:
            return tauth(vtoken, username)['response']
        current_user = tauth(vtoken, username)['response']
        following = self.request.data.get('following')
        if type(following) != int:
            try:
                following = int(following)
                if not User.objects.filter(id=following).exists():
                    if not User.objects.filter(username=str(following)).exists():
                        return Response({'status': 'Denied', 'reason': 'The user you are trying to follow is invalid!'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        following = User.objects.get(username=following)
                else:
                    following = User.objects.get(id=following)
            except:
                if not User.objects.filter(username=following).exists():
                    return Response({'status': 'Denied', 'reason': 'The user you are trying to follow is invalid!'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    following = User.objects.get(username=following)
        followcall = {
            'follower': current_user.id,
            'following': following.id
        }
        FollowSerializer = FollowSerial(data=followcall)
        if FollowSerializer.is_valid():
            FollowSerializer.save()
            return Response({'status': 'Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Denied', 'reason': FollowSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
