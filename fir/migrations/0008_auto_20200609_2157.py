# Generated by Django 3.0.7 on 2020-06-09 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fir', '0007_auto_20200609_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='fir',
            name='put_in_ssp_office',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='fir',
            name='put_in_ssp_office_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
