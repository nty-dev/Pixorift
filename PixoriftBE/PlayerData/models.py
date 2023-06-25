from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class PlayerData(models.Model):
    player = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, unique=True)
    level = models.IntegerField(blank=False, default=1)
    xp = models.IntegerField(blank=False, default=0)

    def xp_gain(self, amount):
        self.xp = self.xp + amount
        if self.xp > 999:
            addedlvl = int(self.xp/1000)
            self.xp = self.xp%1000
            self.level = self.level + addedlvl
        self.save()

    class Meta:
        ordering = ['level', 'xp']
