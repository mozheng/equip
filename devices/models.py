#-*- coding:utf-8 -*-

from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Program(models.Model):
    name = models.CharField(max_length=30)
    url = models.URLField(default="")

    def __unicode__(self):
        return self.name

STATECHOICE = (
        ('E', 'Empty'),
        ('B', 'Broken'),
        ('S', 'Stop'),
        ('R', 'Running'),
    )


class Devices(models.Model):
    name = models.CharField(max_length=30)
    corporation = models.CharField(max_length=100)
    state = models.CharField(max_length=1, choices=STATECHOICE, default='E')
    assessment_program = models.ForeignKey(Program)
    description = models.TextField()
    manual = models.TextField()
    imageURL = models.URLField(default="")

    def __unicode__(self):
        return self.name