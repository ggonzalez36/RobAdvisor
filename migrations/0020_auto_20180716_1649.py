# Generated by Django 2.0.6 on 2018-07-16 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('robadv', '0019_auto_20180716_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='companyFK',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='robadv.Company'),
        ),
    ]
