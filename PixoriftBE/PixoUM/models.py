from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from PlayerData.levels import *
from django.core.exceptions import ValidationError

User = get_user_model()

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name='followers')
    following = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name='following')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following',], name='Follow-Once', )
        ]

    def clean(self, *args, **kwargs):
        if self.follower == self.following:
            raise ValidationError(
                {'Self-Follow': 'You cannot follow youself!'},
            )
        return super(Follow, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Follow, self).save(*args, **kwargs)
