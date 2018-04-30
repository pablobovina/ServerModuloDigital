# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

#### MOCK
import datetime
import json
import uuid
from random import randrange, choice
#### MOCK


def create_experiment(request):
    return HttpResponse("Vista create_experiment")


def read_experiment(request):
    return HttpResponse("Vista read_experiment")


def delete_experiment(request):
    return HttpResponse("Vista delete_experiment")


def update_experiment(request):
    return HttpResponse("Vista update_experiment")

@login_required
def experiment_switch(request, username, experiment):

    print username
    print str(experiment)

    def random_date(start, l):
        current = start
        while l >= 0:
            curr = current + datetime.timedelta(minutes=randrange(60))
            yield curr
            l -= 1

    n_users = 10
    startDate = datetime.datetime(2013, 9, 20, 13, 00)
    authors = ["pbovina", "lmessi", "jreno", "jpmorgan", "dtrump", "cfk"]
    descr = ["atado con alambre", "el mejor experiemento", "casi lo termino", "ni Albert lo podia hacer mejor",
             "no salio bien"]
    states = ["en edicion", "en ejcucion", "finalizado", "cancelado"]
    d = []
    for i in range(n_users):
        d.append({"id": str(uuid.uuid4()),
                  "created": [x for x in random_date(startDate, 1)][0].strftime("%c"),
                  "author": choice(authors),
                  "resume": choice(descr),
                  "state": choice(states)})
    dd = {"error": False, "msg": "tu consulta no esta permitida", "username": "jperez", "authError": False, "datas": d}
    j = json.dumps(dd)
    return HttpResponse(j, content_type="application/json")
