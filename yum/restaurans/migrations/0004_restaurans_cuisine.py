# Generated by Django 4.2.14 on 2024-10-21 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurans', '0003_restaurans_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurans',
            name='cuisine',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurans.cuisine', verbose_name='Кухня'),
        ),
    ]
