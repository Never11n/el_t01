# Generated by Django 3.2.8 on 2023-11-06 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('el_t01_app', '0004_list_external_company_settings'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone_code',
            field=models.CharField(blank=True, default='', max_length=10, null=True),
        ),
    ]
