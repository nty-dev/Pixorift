from django.shortcuts import render
from .PixoAI import PixoAI as P
from django.core.files.storage import FileSystemStorage, Storage
from UserInfo.tauth import tauth
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model, authenticate
from django.core import serializers
from PlayerData.models import *
from .serializers import *
from .models import *
from random import *
from .questlist import *
from datetime import *
import pytz
import base64 as b64
from django.core.files.base import ContentFile
# Create your views here.

User = get_user_model()
quest_refresh_hours = 4

def convert_timedelta(td_field):
    seconds = td_field.seconds
    days = td_field.days
    total_seconds = days*86400 + seconds
    return total_seconds

def checksum(PQ, current_player):
    check = PQ.state
    if check:
        return [check, PQ.get_questitem_display()]
    else:
        last_used = PQ.lastused
        time_now = datetime.utcnow()
        time_now = time_now.replace(tzinfo=pytz.utc)
        time_diff = convert_timedelta(time_now - last_used)
        hours_diff = int(time_diff / 3600)
        if hours_diff >= quest_refresh_hours:
            QuestObj = Quests.objects.get(player=current_player)
            QuestList = [QuestObj.quest1, QuestObj.quest2, QuestObj.quest3]
            quest_generation(QuestList, PQ, False)
            return [True, PQ.get_questitem_display()]
        else:
            time_diff = quest_refresh_hours * 3600 - time_diff
            hours = int(time_diff / 3600)
            minutes = int((time_diff % 3600)/60)
            seconds = int(time_diff % 60)
            return [check, {'h': hours, 'm': minutes, 's': seconds}]

def quest_generation(qlist, cquest, state=True):
    questl = questlist()
    questlst = [x[0] for x in questl]
    for i in qlist:
        if i.state:
            questlst.remove(i.questitem)
    if state:
        questlst.remove(cquest.questitem)
    cquest.questitem = choice(questlst)
    cquest.state = True
    cquest.save()

def create_playerquest(current_player):
    questl = questlist()
    questlst = [x[0] for x in questl]
    insert_quest = list()
    for i in range(3):
        quest = PlayerQuest.objects.create(questitem=choice(questlst))
        questlst.remove(quest.questitem)
        insert_quest.append(quest)
    Quests.objects.create(player=current_player, quest1=insert_quest[0], quest2=insert_quest[1], quest3=insert_quest[2])

def gather_quests(current_player):
    current_quest = Quests.objects.get(player=current_player)
    QuestList = [current_quest.quest1, current_quest.quest2, current_quest.quest3]
    p = list()
    for i in QuestList:
        ret = checksum(i, current_player)
        if ret[0]:
            p.append({'state': True, 'Quest': ret[1]})
        else:
            p.append({'state': False, 'Time': ret[1]})
    return {'Quest1': p[0], 'Quest2': p[1], 'Quest3': p[2]}


class ImageSubmit(APIView):
    def post(self, request):
        username = self.request.data.get('username')
        vtoken = self.request.data.get('Auth')
        if not tauth(vtoken, username)['status']:
            return tauth(vtoken, username)['response']
        current_user = tauth(vtoken, username)['response']
        submitquest = self.request.data.get('Quest')
        if submitquest == None:
            return Response({'status': 'Failed', 'Reason': 'Did not send quest number!'}, status=status.HTTP_400_BAD_REQUEST)
        #relook at this hardcode
        if submitquest != '1' and submitquest != '2' and submitquest != '3':
            return Response({'status': 'Failed', 'Reason': 'Invalid Quest Number!'}, status=status.HTTP_400_BAD_REQUEST)
        if TempImageUpload.objects.filter(player=current_user).exists():
            TempImageUpload.objects.get(player=current_user).delete()
        QuestObject = Quests.objects.get(player=current_user)
        QuestTransfer = [QuestObject.quest1, QuestObject.quest2, QuestObject.quest3]
        PQobj = QuestTransfer.pop(int(submitquest) - 1)
        return_checksum = checksum(PQobj, current_user)
        if not return_checksum[0]:
            return Response({'status': 'Success', 'Quest': 'Failed', 'Reason': 'Quest on cooldown!', 'Time': return_checksum[1]})
        image_uploaded = self.request.data.get('submit')
        format, imgstr = image_uploaded.split(';base64,')
        ext = format.split('/')[-1]
        image_uploaded = ContentFile(b64.b64decode(imgstr), name=current_user.username + '_Image.' + ext)
        image_info = ImageValidation(data={'player': current_user.pk, 'imagefile': image_uploaded})
        if image_info.is_valid():
            image_info.save()
            process_path = TempImageUpload.objects.get(player=current_user).imagefile.path
            temp_proc = False
            try:
                PixoAI = P()
                AIcheck = PixoAI.checksum()
                if not AIcheck[0]:
                    TempImageUpload.objects.get(player=current_user).delete()
                    return Response({'status': 'Denied', 'Reason': AIcheck[1]})
                returnval = PixoAI.process(process_path)
            except:
                try:
                    PixoAI = P()
                    AIcheck = PixoAI.checksum()
                    if not AIcheck[0]:
                        TempImageUpload.objects.get(player=current_user).delete()
                        return Response({'status': 'Denied', 'Reason': AIcheck[1]})
                    returnval = PixoAI.process(process_path)
                except:
                    temp_proc = True
            TempImageUpload.objects.get(player=current_user).delete()
            if temp_proc:
                return Response({'status': 'Success', 'Quest': 'Failed', 'Reason': 'Fatal Error occurred during Image Processing, please re-submit your picture.'})
            if not Quests.objects.filter(player=current_user).exists():
                create_playerquest(current_user)
            if int(returnval[1]) < 45:
                return Response({'status': 'Success', 'Quest': 'Failed', 'Reason': 'Image does not fit quest requirements!'})
            if PQobj.get_questitem_display().lower() != returnval[0].lower():
                return Response({'status': 'Success', 'Quest': 'Failed', 'Reason': 'Image does not fit quest requirements!'})
            else:
                if not PlayerData.objects.filter(player=current_user).exists():
                    PlayerData.objects.create(player=current_user)
                PQobj.state = False
                PQobj.lastused = datetime.utcnow()
                PQobj.save()
                pd = PlayerData.objects.get(player=current_user)
                expgain = 100 + randint(1, 300)
                pd.xp_gain(expgain)
                return Response({'status': 'Success', 'Quest': 'Success', 'Reason': 'Quest ' + submitquest + ' completed!', 'XP_Gain': expgain, 'PlayerData': {'Level': pd.level, 'XP': pd.xp}, 'NextQuest': gather_quests(current_user)})
        return Response({'status': 'Denied', 'Error': 'Image File Missing or Invalid.', 'info': image_info.errors})

class QuestRequest(APIView):
    def get(self, request):
        username = self.request.GET.get('username')
        vtoken = self.request.GET.get('Auth')
        if not tauth(vtoken, username)['status']:
            return tauth(vtoken, username)['response']
        current_user = tauth(vtoken, username)['response']
        if Quests.objects.filter(player=current_user).exists():
            return Response({'status': 'Success', 'Quest': gather_quests(current_user)})
        else:
            create_playerquest(current_user)
            return Response({'status': 'Success', 'Quest': gather_quests(current_user)})
