# Generated by Django 4.2.6 on 2024-03-14 05:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_designlisimap'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='designlisimap',
            name='excel_li_si',
        ),
        migrations.RemoveField(
            model_name='designlisimap',
            name='map_li_si_pr',
        ),
    ]
