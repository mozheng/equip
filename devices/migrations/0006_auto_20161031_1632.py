# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-31 08:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0005_devices_imageurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devices',
            name='imageURL',
            field=models.URLField(default=''),
        ),
        migrations.AlterField(
            model_name='program',
            name='url',
            field=models.URLField(default=''),
        ),
    ]
