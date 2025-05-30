# Generated by Django 4.2.14 on 2025-03-02 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='latitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Широта'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='longitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Долгота'),
        ),
    ]
