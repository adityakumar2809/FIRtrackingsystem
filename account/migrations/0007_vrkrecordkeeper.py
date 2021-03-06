# Generated by Django 3.0.7 on 2020-06-10 23:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0006_auto_20200610_2208'),
    ]

    operations = [
        migrations.CreateModel(
            name='VRKRecordKeeper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vrk_record_keepers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'VRK Record Keeper',
                'verbose_name_plural': 'VRK Record Keepers',
            },
        ),
    ]
