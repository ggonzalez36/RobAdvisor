# Generated by Django 2.0.6 on 2018-07-04 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robadv', '0007_auto_20180704_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='change',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='company',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
