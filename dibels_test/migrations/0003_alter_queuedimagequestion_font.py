# Generated by Django 4.0.3 on 2022-07-12 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dibels_test', '0002_alter_queuedmazequestion_font'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queuedimagequestion',
            name='font',
            field=models.ForeignKey(default=134, on_delete=django.db.models.deletion.CASCADE, to='dibels_test.font'),
        ),
    ]
