# Generated by Django 4.2.14 on 2025-03-10 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurans', '0006_restaurans_latitude_restaurans_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurans',
            name='rating',
            field=models.FloatField(null=True, verbose_name='Рейтинг (звезды)'),
        ),
    ]
