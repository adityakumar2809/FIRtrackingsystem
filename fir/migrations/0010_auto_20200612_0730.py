# Generated by Django 3.0.7 on 2020-06-12 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fir', '0009_auto_20200610_0700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fir',
            name='date_created',
            field=models.DateField(auto_now_add=True),
        ),
    ]
