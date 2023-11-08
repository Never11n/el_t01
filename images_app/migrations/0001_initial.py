# Generated by Django 2.2.6 on 2020-05-29 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin', models.URLField(default='')),
                ('thumb', models.URLField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='ImageFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=256)),
                ('content_type', models.CharField(max_length=256)),
                ('size', models.IntegerField(default=0)),
            ],
        ),
    ]