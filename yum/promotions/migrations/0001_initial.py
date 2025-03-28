# Generated by Django 4.2.14 on 2024-10-17 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('restaurans', '0003_restaurans_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('description', models.TextField(max_length=200, verbose_name='Описание акции')),
                ('start_time', models.DateTimeField(auto_now_add=True, verbose_name='Дата начала акции')),
                ('end_time', models.DateTimeField(auto_now_add=True, verbose_name='Дата конца акции')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurans.restaurans', verbose_name='Ресторан')),
            ],
            options={
                'verbose_name': 'Акция',
                'verbose_name_plural': 'Акции',
                'db_table': 'promotion',
            },
        ),
    ]
