# Generated by Django 3.0.7 on 2020-06-27 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firBeta', '0003_auto_20200624_0139'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='firphase',
            options={'ordering': ['-fir__pk', 'phase_index'], 'verbose_name': 'FIR Phase', 'verbose_name_plural': 'FIR Phases'},
        ),
    ]
