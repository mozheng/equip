# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-08 09:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='devices',
            old_name='assessment_programme',
            new_name='assessment_program',
        ),
    ]