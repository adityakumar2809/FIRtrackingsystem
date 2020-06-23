# Generated by Django 3.0.7 on 2020-06-23 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0001_initial'),
        ('firBeta', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fir',
            options={'ordering': ['sub_division', 'police_station', '-fir_no'], 'verbose_name': 'FIR', 'verbose_name_plural': 'FIRs'},
        ),
        migrations.AlterModelOptions(
            name='firphase',
            options={'ordering': ['-fir', 'phase_index'], 'verbose_name': 'FIR Phase', 'verbose_name_plural': 'FIR Phases'},
        ),
        migrations.AlterUniqueTogether(
            name='fir',
            unique_together={('sub_division', 'police_station', 'fir_no')},
        ),
        migrations.AlterUniqueTogether(
            name='firphase',
            unique_together={('fir', 'phase_index')},
        ),
    ]
