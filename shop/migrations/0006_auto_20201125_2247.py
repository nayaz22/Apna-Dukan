# Generated by Django 3.0.8 on 2020-11-26 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_orders'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='items_Json',
        ),
        migrations.AddField(
            model_name='orders',
            name='itemsJson',
            field=models.CharField(default='', max_length=5000),
        ),
    ]