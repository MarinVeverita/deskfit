from rest_framework import serializers
from .models import ActiveBreaksSettings, Workout, Exercise, WorkoutExercise, PlannedWorkout

class ActiveBreaksSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveBreaksSettings
        fields = ['work_duration', 'break_duration', 'auto_start_work_timer', 'auto_start_break_timer']


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['name', 'muscle', 'difficulty', 'equipment', 'instructions', 'type']


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer()

    class Meta:
        model = WorkoutExercise
        fields = ['exercise', 'sets', 'repetitions', 'work_time', 'rest_time']

class WorkoutSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(many=True)

    class Meta:
        model = Workout
        fields = ['id', 'name', 'exercises']


class PlannedWorkoutSerializer(serializers.ModelSerializer):
    workout = serializers.PrimaryKeyRelatedField(queryset=Workout.objects.all())

    class Meta:
        model = PlannedWorkout
        fields = ['day_of_week', 'workout']
        read_only_fields = ['user']


