# Generated by Django 2.0.6 on 2018-07-13 16:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robadv', '0013_performance'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='creationDate',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='lastUpdate',
            field=models.DateField(default=datetime.date.today),
        ),
    ]