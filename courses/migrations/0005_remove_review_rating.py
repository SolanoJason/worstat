# Generated by Django 4.2.8 on 2024-01-21 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_alter_course_options_alter_enrollment_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='rating',
        ),
    ]
