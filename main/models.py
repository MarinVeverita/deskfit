from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import models
from django.utils import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver


class ActiveBreaksSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    work_duration = models.FloatField(default=25)  #time in min
    break_duration = models.FloatField(default=3)   #time in min
    auto_start_work_timer = models.BooleanField(default=False)
    auto_start_break_timer = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + "'s Active Breaks Settings"
     

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Workout: {self.name} by {self.user}"



class Exercise(models.Model):
    name = models.CharField(max_length=100)
    muscle = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=50, null=True, blank=True)
    equipment = models.CharField(max_length=100, null=True, blank=True)
    instructions = models.TextField()
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField()
    repetitions = models.IntegerField()
    work_time = models.DurationField()
    rest_time = models.DurationField()

    def __str__(self):
        return f"{self.exercise.name} for {self.workout.name}"


class PlannedWorkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ])
    workout = models.ForeignKey(Workout, on_delete=models.SET_NULL, null=True, blank=True)
    

    def __str__(self):
        return f"Planned workout for {self.day_of_week} by {self.user}"



@receiver(post_save, sender=User)
def create_active_breaks_settings(sender, instance, created, **kwargs):
    if created:
        ActiveBreaksSettings.objects.create(user=instance)