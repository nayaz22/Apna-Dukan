# Generated by Django 3.0.8 on 2020-11-15 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20201115_1117'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='city',
            new_name='country',
        ),
        migrations.AlterField(
            model_name='contact',
            name='cel',
            field=models.CharField(default='', max_length=50),
        ),
    ]
