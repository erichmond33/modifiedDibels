# Generated by Django 3.2.9 on 2022-01-14 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dibels_test', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagetest',

            field=models.TextField(default='null'),
        ),
        migrations.AddField(
            model_name='imagetest',
            name='gradeLevel',
            field=models.CharField(default='null', max_length=20),
        ),
        migrations.AddField(
            model_name='mazetest',

            field=models.TextField(default='null'),
        ),
        migrations.AddField(
            model_name='mazetest',
            name='gradeLevel',
            field=models.CharField(default='null', max_length=20),
        ),
    ]
