from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from PlayerData.levels import *

User = get_user_model()

class PlayerData(models.Model):
    player = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, unique=True, related_name='playerdata_set')
    level = models.IntegerField(blank=False, default=1)
    xp = models.IntegerField(blank=False, default=0)
    totalxp = models.IntegerField(blank=False, default=0)

    def xp_edit(self, amount):
        if type(amount) != int:
            raise TypeError('Amount must be an integer!')
        self.totalxp = self.totalxp + amount
        if self.totalxp <= 0:
            self.totalxp = 0
            self.xp = 0
            self.level = 1
        else:
            self.xp = self.xp + amount
            iter = True
            while iter:
                if self.xp < 0:
                    self.level = self.level - 1
                    self.xp = self.xp + lvl2xp(self.level)
                else:
                    lvl_req = lvl2xp(self.level)
                    if self.xp >= lvl_req:
                        self.xp = self.xp - lvl_req
                        self.level = self.level + 1
                    else:
                        iter = False
        self.save()

    def exp(self, amount):
        if type(amount) != int:
            raise TypeError('Amount must be an integer!')
        if amount < 0:
            raise AssertionError('Amount must be more than 0!')
        self.totalxp = self.totalxp + amount
        self.xp = self.xp + amount
        iter = True
        while iter:
            lvl_req = lvl2xp(self.level)
            if self.xp >= lvl_req:
                self.xp = self.xp - lvl_req
                self.level = self.level + 1
            else:
                iter = False
        self.save()

    def level_edit(self, amount):
        if type(amount) != int:
            raise TypeError('Amount must be an integer!')
        level_xp_ratio = self.xp/lvl2xp(self.level)
        self.level = self.level + amount
        if self.level < 1:
            self.totalxp = 0
            self.xp = 0
            self.level = 1
        else:
            self.xp = int(level_xp_ratio*lvl2xp(self.level))
            self.totalxp = totalxp(self.level, self.xp)
        self.save()

    def fullxp(self):
        return lvl2xp(self.level)

    class Meta:
        ordering = ['totalxp', 'level', 'xp']
