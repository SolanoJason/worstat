# Generated by Django 4.2.8 on 2024-01-21 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='about',
            field=models.TextField(blank=True, verbose_name='Biografia'),
        ),
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Correo electronico'),
        ),
        migrations.AlterField(
            model_name='account',
            name='full_name',
            field=models.CharField(max_length=150, verbose_name='Nombre completo'),
        ),
    ]
