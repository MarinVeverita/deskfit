# Generated by Django 5.0.2 on 2024-03-06 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_rename_work_duration_activebreakssettings_break_timer_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activebreakssettings',
            old_name='break_timer',
            new_name='break_duration',
        ),
        migrations.RenameField(
            model_name='activebreakssettings',
            old_name='work_timer',
            new_name='work_duration',
        ),
    ]
