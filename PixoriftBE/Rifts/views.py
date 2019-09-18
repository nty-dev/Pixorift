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
from PixoUM.models import *
from .serializers import *
from .models import *
# Create your views here.
User = get_user_model()

class RiftView(APIView):
    def get(self, request):
        NUMBER_PER_PAGE = 5
        username = self.request.GET.get('username')
        vtoken = self.request.GET.get('Auth')
        page = self.request.GET.get('page')
        if not tauth(vtoken, username)['status']:
            return tauth(vtoken, username)['response']
        current_user = tauth(vtoken, username)['response']
        if page is None or page is '':
            page = 1
        if type(page) != int:
            try:
                page = int(page)
            except:
                return Response({'status': 'Denied', 'reason': 'Page must be an integer!'}, status=status.HTTP_400_BAD_REQUEST)
        pag = page - 1
        UserRift = current_user.rift_set.order_by('-upload_date')[pag*NUMBER_PER_PAGE:page*NUMBER_PER_PAGE]
        UserRiftRet = DRiftSerial(UserRift, many=True)
        return Response({'status': 'Success', 'rifts': UserRiftRet.data}, status=status.HTTP_200_OK)

    def post(self, request):
        username = self.request.data.get('username')
        vtoken = self.request.data.get('Auth')
        if not tauth(vtoken, username)['status']:
            return tauth(vtoken, username)['response']
        current_user = tauth(vtoken, username)['response']
        if self.request.data.get('content') == None:
            content = ''
        else:
            content = self.request.data.get('content')
        riftpost = {
            'author': current_user.id,
            'content': content,
            'images': [{'image': i} for i in self.request.data.getlist('images')],
        }
        RiftPost = URiftSerial(data=riftpost)
        if RiftPost.is_valid():
            RiftPost.save()
            return Response({'status': 'Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Denied', 'reason': RiftPost.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        username = self.request.data.get('username')
        vtoken = self.request.data.get('Auth')
        if not tauth(vtoken, username)['status']:
            return tauth(vtoken, username)['response']
        current_user = tauth(vtoken, username)['response']
        riftid = self.request.data.get('rift')
        if type(riftid) != int:
            try:
                riftid = int(riftid)
            except:
                return Response({'state': 'Denied', 'reason': 'Invalid Rift ID!'}, status=status.HTTP_400_BAD_REQUEST)
        if not Rift.objects.filter(id=riftid).exists():
            return Response({'state': 'Denied', 'reason': 'Invalid Rift ID!'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'e':'e'})

class RiftRatingView(APIView):
    def post(self, request):
        username = self.request.data.get('username')
        vtoken = self.request.data.get('Auth')
        if not tauth(vtoken, username)['status']:
            return tauth(vtoken, username)['response']
        current_user = tauth(vtoken, username)['response']
        rate = self.request.data.get('rate')
        if rate == None or rate == '':
            pass
        elif rate.lower() in ['t', 'true', 'up', '1']:
            rate = True
        elif rate.lower() in ['f', 'false', 'down', '0']:
            rate = False
        else:
            rate = None
        riftid = self.request.data.get('rift')
        if type(riftid) != int:
            try:
                riftid = int(riftid)
            except:
                return Response({'state': 'Denied', 'reason': 'Invalid Rift ID!'}, status=status.HTTP_400_BAD_REQUEST)
        if not Rift.objects.filter(id=riftid).exists():
            return Response({'state': 'Denied', 'reason': 'Invalid Rift ID!'}, status=status.HTTP_400_BAD_REQUEST)
        RiftRate = {
            'rater': current_user.id,
            'rift': riftid,
            'rating': rate
        }
        if RiftRating.objects.filter(rater=current_user.id, rift=riftid).exists():
            RiftRateS = RiftRatingSerial(data=RiftRate, instance=RiftRating.objects.get(rater=current_user.id, rift=riftid))
        else:
            RiftRateS = RiftRatingSerial(data=RiftRate)
        if RiftRateS.is_valid():
            RiftRateS.save()
            return Response({'status': 'Success', 'info': {'rate': rate, 'rift': riftid}}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Denied', 'reason': RiftRateS.errors}, status=status.HTTP_400_BAD_REQUEST)
