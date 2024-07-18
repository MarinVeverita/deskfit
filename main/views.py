from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
import requests
 
from .forms import RegistrationForm

from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ActiveBreaksSettings, Workout, Exercise, WorkoutExercise, PlannedWorkout
from .serializers import ActiveBreaksSettingsSerializer, WorkoutSerializer, PlannedWorkoutSerializer


from django.contrib.auth.models import User
from .models import ActiveBreaksSettings

from dotenv import load_dotenv
import os

from datetime import timedelta

load_dotenv()


NINJA_API_KEY = os.environ.get('NINJA_API_KEY')

def home(request):
    return render(request, "main/home.html")


def active_breaks(request):
    return render(request, "main/active_breaks.html")


def plan_workout(request):
    return render(request, "main/plan_workout.html")

def workout_of_the_day(request):
    return render(request, "main/workout_of_the_day.html")

def create_workout(request):
    return render(request, "main/create_workout.html")


def get_exercises(request):
     if request.method == 'GET':
        muscles = request.GET.getlist('muscleGroups[]')
        exercises = []

        for muscle in muscles:
            api_url = 'https://api.api-ninjas.com/v1/exercises?muscle={}'.format(muscle)
            response = requests.get(api_url, headers={'X-Api-Key': NINJA_API_KEY})

            if response.status_code == requests.codes.ok:
                muscle_exercises = response.json()
                exercises.extend(muscle_exercises)
            
            else:
                print("Error:", response.status_code, response.text)
        
        return JsonResponse({'exercises': exercises})


def search_exercise(request):
    if request.method == 'GET':
        name = request.GET['name']
        exercises = {}
    
        api_url = 'https://api.api-ninjas.com/v1/exercises?name={}'.format(name)
        response = requests.get(api_url, headers={'X-Api-Key': NINJA_API_KEY})

        if response.status_code == requests.codes.ok:
            exercises = response.json()
        else:
            print("Error:", response.status_code, response.text)

        return JsonResponse({'exercises': exercises})
    



class WorkoutViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Workout.objects.filter(user=user).prefetch_related('exercises__exercise')
    





class PlannedWorkoutViewSet(viewsets.ModelViewSet):
    queryset = PlannedWorkout.objects.all()
    serializer_class = PlannedWorkoutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        workout_id = self.request.data.get('workout')
        workout = Workout.objects.get(id=workout_id)
        serializer.save(user=self.request.user, workout=workout)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data

        new_day_of_week = data.get('day_of_week')
        if new_day_of_week and new_day_of_week != instance.day_of_week:
            PlannedWorkout.objects.filter(user=request.user, day_of_week=new_day_of_week).delete()

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='week-plan')
    def week_plan(self, request):
        user = request.user
        planned_workouts = PlannedWorkout.objects.filter(user=user)

        week_plan = {day: None for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']}
        for pw in planned_workouts:
            if pw.workout:
                workout_serializer = WorkoutSerializer(pw.workout)
                week_plan[pw.day_of_week] = workout_serializer.data

        return Response(week_plan)

    def destroy(self, request, *args, **kwargs):
        day_of_week = request.data.get('day')
        if not day_of_week:
            return Response({"error": "Day of week is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        planned_workout = get_object_or_404(PlannedWorkout, user=request.user, day_of_week=day_of_week)
        self.perform_destroy(planned_workout)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

        



@login_required
def save_workout(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    try:
        data = json.loads(request.body)

        workout_name = data.get('workout_name')
        exercises = data.get('exercises')

        # Create the workout
        workout = Workout.objects.create(user=request.user, name=workout_name)

        for exercise_data in exercises:
            exercise, created = Exercise.objects.get_or_create(
                name=exercise_data['name'],
                defaults={
                    'muscle': exercise_data['details']['muscle'],
                    'difficulty': exercise_data['details'].get('difficulty', ''),
                    'equipment': exercise_data['details'].get('equipment', ''),
                    'instructions': exercise_data['details'].get('instructions', ''),
                    'type': exercise_data['details']['type']
                }
            )

            # Convert string durations to timedelta objects
            work_time = timedelta(seconds=int(exercise_data['work_time']))
            rest_time = timedelta(seconds=int(exercise_data['rest_time']))

            WorkoutExercise.objects.create(
                workout=workout,
                exercise=exercise,
                sets=int(exercise_data['sets']),
                repetitions=int(exercise_data['reps']),
                work_time=work_time,
                rest_time=rest_time
            )

        return JsonResponse({"message": "Workout saved successfully."}, status=200)
    
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", str(e))
        return JsonResponse({"error": "Invalid JSON format."}, status=400)
    except Exception as e:
        print("General Error:", str(e))  # Log the error message
        return JsonResponse({"error": str(e)}, status=500)

class ActiveBreaksSettingsAPIView(generics.ListAPIView):
    serializer_class = ActiveBreaksSettingsSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = ActiveBreaksSettings.objects.filter(user=user)
        return queryset


    

def updateActiveBreaksSettings(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    try:
        data = json.loads(request.body)
        username = data.get('username')
        new_settings = data.get('settings')[0]

        user = User.objects.get(username=username)
        settings = ActiveBreaksSettings.objects.get(user=user)

        for key, value in new_settings.items():
            setattr(settings, key, value)
        settings.save()

        return JsonResponse({"message": "Settings updated successfully."}, status=200)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    





def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, "registration/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "registration/login.html")
 


def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    
    else:
        form = RegistrationForm()

    return render(request, 'registration/sign_up.html', {'form': form})
