# Generated by Django 3.2.9 on 2022-02-05 00:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dibels_test', '0011_auto_20220205_0017'),
    ]

    operations = [
        migrations.CreateModel(
            name='queuedMazeQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('queuedSentenceId', models.IntegerField(default='-1')),
                ('queuedWordSelection', models.CharField(blank=True, max_length=50)),
                ('queuedGeneratedWord1', models.CharField(blank=True, max_length=50)),
                ('queuedGeneratedWord2', models.CharField(blank=True, max_length=50)),
                ('testId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dibels_test.mazetest')),
            ],
        ),
    ]