# Generated by Django 2.0.6 on 2018-07-01 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robadv', '0005_transaction_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='assetId',
            field=models.IntegerField(default=0),
        ),
    ]
