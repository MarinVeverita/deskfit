from django.urls import path
from . import views
from .views import ActiveBreaksSettingsAPIView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.conf import settings

from django.views.generic import TemplateView


urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('active-breaks', views.active_breaks, name="active_breaks"),
    path('plan-workout', views.plan_workout, name="plan_workout"),

    path('updateActiveBreaksSettings', views.updateActiveBreaksSettings, name="updateActiveBreaksSettings"),
    path('api/active-breaks-settings/', ActiveBreaksSettingsAPIView.as_view(), name='active-breaks-settings-api'),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),

    path('hello-webpack/', TemplateView.as_view(template_name='hello_webpack.html'))
 ]