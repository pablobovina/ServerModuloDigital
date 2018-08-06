# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
# import sys
# sys.path.append("C:\\Users\\pablo\\Downloads\\tesis\\repo\ModuloDigital")

from ModuloDigital.source.experiment_reporter import ExperimentReporter
from ModuloDigital.source.experiment_scanner import ExperimentScanner
import json


def run_experiment(request, username, experiment):
    print "corremos experimento"
    experiments = request.session["experiments"]
    d = experiments[username][experiment]
    try:
        experiment_scn = ExperimentScanner(d)
        experiment_rep = ExperimentReporter(experiment_scn)
        for exp in experiment_rep:
            print exp
    except Exception as e:
        msg = [e.message]
        return HttpResponse(json.dumps(msg), content_type="application/json", status=500)
    return HttpResponse("Vista run_experiment")


def stop_experiment(request):
    return HttpResponse("Vista stop_experiment")


def status_experiment(request):
    return HttpResponse("Vista status_experiment")


def run_queue_experiment(request):
    return HttpResponse("Vista run_queue_experiment")
