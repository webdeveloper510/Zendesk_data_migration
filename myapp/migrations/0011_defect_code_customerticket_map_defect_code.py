# Generated by Django 4.2.6 on 2024-03-15 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_customerticket_map_design_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Defect_code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('map_defect_code', models.CharField(blank=True, max_length=300, null=True)),
                ('excel_defect_code', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='customerticket',
            name='map_defect_code',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]