# Generated by Django 4.2.14 on 2024-10-24 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_alter_dish_restaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='dishes_images', verbose_name='Изображение'),
        ),
    ]
