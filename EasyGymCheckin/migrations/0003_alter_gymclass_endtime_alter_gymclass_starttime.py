# Generated by Django 4.2.10 on 2024-02-25 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EasyGymCheckin', '0002_gymcheckin_successful'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gymclass',
            name='endTime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='gymclass',
            name='startTime',
            field=models.DateTimeField(),
        ),
    ]