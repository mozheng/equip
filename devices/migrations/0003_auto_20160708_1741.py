# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-08 09:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0002_auto_20160708_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='url',
            field=models.TextField(),
        ),
    ]