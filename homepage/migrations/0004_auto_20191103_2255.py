# Generated by Django 2.2.6 on 2019-11-03 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0003_auto_20191103_2227'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userrequest',
            old_name='cuisine',
            new_name='cuisines',
        ),
    ]
