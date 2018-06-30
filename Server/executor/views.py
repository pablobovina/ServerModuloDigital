# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
import sys
sys.path.append("C:\\Users\\pablo\\Downloads\\tesis\\repo\ModuloDigital")

from experiment2 import Experiment


def run_experiment(request, username, experiment):
    print "corremos experimento"
    experiments = request.session["experiments"]
    d = experiments[username][experiment]
    ex = Experiment(d)
    ex.run()
    for e in ex:
        ex.run()
        print "_" * 80
    return HttpResponse("Vista run_experiment")


def stop_experiment(request):
    return HttpResponse("Vista stop_experiment")


def status_experiment(request):
    return HttpResponse("Vista status_experiment")


def run_queue_experiment(request):
    return HttpResponse("Vista run_queue_experiment")
