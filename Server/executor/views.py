# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from ModuloDigital.main import main
import json


def run_experiment(request, username, experiment):
    print "corremos experimento"
    experiments = request.session["experiments"]
    d = experiments[username][experiment]
    try:
        main(d)

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
