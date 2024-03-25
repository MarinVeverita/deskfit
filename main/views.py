from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

from .forms import RegistrationForm

from rest_framework import generics
from .models import ActiveBreaksSettings
from .serializers import ActiveBreaksSettingsSerializer

from django.contrib.auth.models import User
from .models import ActiveBreaksSettings


def home(request):
    return render(request, "main/home.html")


def active_breaks(request):
    return render(request, "main/active_breaks.html")


def plan_workout(request):
    return render(request, "main/plan_workout.html")





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

        print(new_settings)
        for key, value in new_settings.items():
            print(key, value)
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
