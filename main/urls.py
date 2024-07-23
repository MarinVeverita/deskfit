from django.urls import path, include
from . import views
from .views import ActiveBreaksSettingsAPIView, WorkoutViewSet, PlannedWorkoutViewSet
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.conf import settings

from django.views.generic import TemplateView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'workouts', WorkoutViewSet, basename='workout')
router.register(r'planned_workouts', PlannedWorkoutViewSet, basename='planned_workout')

 
urlpatterns = [
    path('', views.home, name='home'),
    path('', include(router.urls)),
    path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('active-breaks', views.active_breaks, name="active_breaks"),
    path('plan-workout', views.plan_workout, name="plan_workout"),
    path('workout-of-the-day', views.workout_of_the_day, name="workout_of_the_day"),
    path('create-workout', views.create_workout, name="create_workout"),


    path('updateActiveBreaksSettings', views.updateActiveBreaksSettings, name="updateActiveBreaksSettings"),
    path('api/active-breaks-settings/', ActiveBreaksSettingsAPIView.as_view(), name='active-breaks-settings-api'),
    path('api/get-exercises/', views.get_exercises, name='get_exercises'),
    path('api/search-exercise/', views.search_exercise, name="search_exercise"),
    path('api/save-workout/', views.save_workout, name="save_workout"),
    #path('api/get-workouts/', views.get_workouts, name="get_workouts"),

    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),),
    path('accounts/', include('django.contrib.auth.urls')),

    #path('hello-webpack/', TemplateView.as_view(template_name='hello_webpack.html'))
 ]