# Generated by Django 3.2.8 on 2023-09-25 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('el_t01_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game_history',
            name='shop_code',
            field=models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Code of shop'),
        ),
        migrations.AddField(
            model_name='game_history',
            name='shop_code1',
            field=models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Code of shop'),
        ),
    ]
