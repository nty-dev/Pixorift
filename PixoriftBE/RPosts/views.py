from django.shortcuts import render
from django.core.files.storage import FileSystemStorage, Storage
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

class RPostView(APIView):
    def get(self, request):
        username = self.request.GET.get('username')
        vtoken = self.request.GET.get('Auth')
        if not tauth(vtoken, username)['status']:
            return tauth(vtoken, username)['response']
        current_user = tauth(vtoken, username)['response']
        post_list = PixoPost.objects.filter(author=current_user)
        response_list = RPostRetrieve(post_list, many=True).data
        return Response({'state': 'Success', 'Posts': response_list})

    def post(self, request):
        username = self.request.data.get('username')
        vtoken = self.request.data.get('Auth')
        if not tauth(vtoken, username)['status']:
            return tauth(vtoken, username)['response']
        current_user = tauth(vtoken, username)['response']
        image_list = self.request.data.get('images')
        try:
            pass
        except TypeError:
            pass
