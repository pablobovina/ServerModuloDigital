# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Experiment(models.Model):
    author = models.TextField()
    experiment = models.TextField()
    date_time = models.DateTimeField()
    resume = models.TextField()
    status = models.TextField()


class Result(models.Model):
    author = models.TextField()
    experiment = models.TextField()
    date_time = models.DateTimeField()
    resume = models.TextField()
    status = models.TextField()
    error = models.TextField()
    log = models.TextField()
    data = models.TextField()


class ManagerThread(models.Model):
    pid = models.IntegerField()
    running = models.BooleanField()
    author = models.TextField()
    id_result = models.IntegerField()
    date_time = models.DateTimeField()
    name = models.TextField()
    killer = models.TextField()

