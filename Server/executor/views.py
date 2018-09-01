# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from ModuloDigital.main import ModDig
from copy import deepcopy
from shutil import rmtree


def run_experiment(request, username, experiment):
    print "corremos experimento"
    experiments = request.session["experiments"]
    d = experiments[username][experiment]
    copy_d = deepcopy(d)
    out_d = "./out/{}".format(username)
    log_d = "./log/{}".format(username)
    error_d = "./error/{}".format(username)
    m = ModDig(copy_d, out_d, log_d, error_d)
    m.setDaemon(True)
    m.start()

    return HttpResponse("Vista run_experiment")


def stop_experiment(request):
    return HttpResponse("Vista stop_experiment")


def status_experiment(request):
    return HttpResponse("Vista status_experiment")


def run_queue_experiment(request):
    return HttpResponse("Vista run_queue_experiment")
