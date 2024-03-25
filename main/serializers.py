from rest_framework import serializers
from .models import ActiveBreaksSettings

class ActiveBreaksSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveBreaksSettings
        fields = ['work_duration', 'break_duration', 'auto_start_work_timer', 'auto_start_break_timer']