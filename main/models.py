from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import models
from django.utils import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver


class ActiveBreaksSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    work_duration = models.FloatField(default=25)  #time in mins
    break_duration = models.FloatField(default=3)   #time in mins
    auto_start_work_timer = models.BooleanField(default=False)
    auto_start_break_timer = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + "'s Active Breaks Settings"
    



@receiver(post_save, sender=User)
def create_active_breaks_settings(sender, instance, created, **kwargs):
    if created:
        ActiveBreaksSettings.objects.create(user=instance)