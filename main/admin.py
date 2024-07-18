from django.contrib import admin

from .models import Workout, Exercise, WorkoutExercise, PlannedWorkout

# Register your models here.

admin.site.register(Workout)
admin.site.register(Exercise)
admin.site.register(WorkoutExercise)
#admin.site.register(PlannedWorkout)
class PlannedWorkoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'workout', 'day_of_week')
    list_filter = ('day_of_week', 'user')
    search_fields = ('user__username', 'workout__name')
    ordering = ('day_of_week',)

admin.site.register(PlannedWorkout, PlannedWorkoutAdmin)
