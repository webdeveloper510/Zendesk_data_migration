# Generated by Django 4.2.6 on 2024-03-13 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_customerticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerticket',
            name='excel_size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer_tickets', to='myapp.excelsize'),
        ),
        migrations.AddField(
            model_name='customerticket',
            name='user_mapping',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer_tickets', to='myapp.usermapping'),
        ),
    ]
