# Generated by Django 4.2.14 on 2025-05-11 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0006_promotionrequest_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotionrequest',
            name='description',
            field=models.TextField(max_length=500, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='promotionrequest',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Название акции'),
        ),
    ]
