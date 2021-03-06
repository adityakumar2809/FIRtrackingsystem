# Generated by Django 2.1.5 on 2020-04-19 12:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_courtrecordkeeper_policestationrecordkeeper_ssprecordkeeper'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courtrecordkeeper',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='court_record_keepers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='policestationrecordkeeper',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='police_station_record_keepers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ssprecordkeeper',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ssp_record_keepers', to=settings.AUTH_USER_MODEL),
        ),
    ]
