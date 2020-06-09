# Generated by Django 3.0.7 on 2020-06-09 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fir', '0006_auto_20200419_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='fir',
            name='under_section',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='fir',
            name='current_status',
            field=models.CharField(blank=True, choices=[('under_investigation', 'Under Investigation'), ('challan_filed', 'Challan Filed'), ('untraced', 'Untraced'), ('cancelled', 'Cancelled')], max_length=50, null=True),
        ),
    ]
