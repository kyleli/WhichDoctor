# Generated by Django 4.2.1 on 2023-06-17 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_rename_settings_formsettings'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FormSettings',
            new_name='FormConfig',
        ),
    ]