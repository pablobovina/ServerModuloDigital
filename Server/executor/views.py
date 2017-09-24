# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse


def run_experiment(request):
    return HttpResponse("Vista run_experiment")


def stop_experiment(request):
    return HttpResponse("Vista stop_experiment")


def status_experiment(request):
    return HttpResponse("Vista status_experiment")


def run_queue_experiment(request):
    return HttpResponse("Vista run_queue_experiment")
