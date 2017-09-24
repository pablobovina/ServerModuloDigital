# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse


def create_experiment(request):
    return HttpResponse("Vista create_experiment")


def read_experiment(request):
    return HttpResponse("Vista read_experiment")


def delete_experiment(request):
    return HttpResponse("Vista delete_experiment")


def update_experiment(request):
    return HttpResponse("Vista update_experiment")
