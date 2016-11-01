# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-09 05:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0003_auto_20160708_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='devices',
            name='state',
            field=models.CharField(choices=[('E', 'Empty'), ('B', 'Broken'), ('S', 'Stop'), ('R', 'Running')], default='E', max_length=1),
        ),
    ]