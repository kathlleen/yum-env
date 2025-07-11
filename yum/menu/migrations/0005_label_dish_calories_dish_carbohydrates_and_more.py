# Generated by Django 4.2.14 on 2025-05-14 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_alter_dish_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('type', models.CharField(choices=[('universal', 'Универсальный'), ('diet', 'Диетический'), ('allergy', 'Аллергия'), ('preference', 'Предпочтение')], max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='dish',
            name='calories',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dish',
            name='carbohydrates',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dish',
            name='composition',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='dish',
            name='fats',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dish',
            name='proteins',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='DishLabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.dish')),
                ('label', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.label')),
            ],
            options={
                'unique_together': {('dish', 'label')},
            },
        ),
        migrations.AddField(
            model_name='dish',
            name='labels',
            field=models.ManyToManyField(related_name='dishes', through='menu.DishLabel', to='menu.label'),
        ),
    ]
