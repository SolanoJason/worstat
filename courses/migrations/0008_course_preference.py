# Generated by Django 4.2.8 on 2024-01-25 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_course_points_required_enrollment_is_completed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='preference',
            field=models.JSONField(default=0, editable=False),
        ),
    ]
