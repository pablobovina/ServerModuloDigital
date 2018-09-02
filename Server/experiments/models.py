# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Experiment(models.Model):
    author = models.TextField()
    experiment = models.TextField()
    date_time = models.DateTimeField()
    resume = models.TextField()
    status = models.TextField()
