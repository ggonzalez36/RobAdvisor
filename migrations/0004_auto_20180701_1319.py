# Generated by Django 2.0.6 on 2018-07-01 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robadv', '0003_auto_20180701_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprojection',
            name='date',
            field=models.DateField(blank=True),
        ),
    ]