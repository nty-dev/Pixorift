from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from random import choice
from .questlist import *
# Create your models here.
User = get_user_model()

def randquest():
    questitems = questlist()
    return choice(questitems)[0]

class TempImageUpload(models.Model):
    player = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    imagefile = models.ImageField(upload_to='imageai/')

class PlayerQuest(models.Model):
    QUEST_ITEMS = questlist()
    questitem = models.CharField(choices=QUEST_ITEMS, default=randquest(), max_length=100)
    lastused = models.DateTimeField(null=True, blank=True)
    state = models.BooleanField(default=True)

class Quests(models.Model):
    player = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    quest1 = models.OneToOneField(PlayerQuest, on_delete=models.CASCADE, unique=True, related_name='quest1', null=True)
    quest2 = models.OneToOneField(PlayerQuest, on_delete=models.CASCADE, unique=True, related_name='quest2', null=True)
    quest3 = models.OneToOneField(PlayerQuest, on_delete=models.CASCADE, unique=True, related_name='quest3', null=True)
