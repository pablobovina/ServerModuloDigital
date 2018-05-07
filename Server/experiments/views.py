# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

#### MOCK
import datetime
import json
import uuid
from random import randrange, choice
from pprint import pprint
#### MOCK


def create_experiment(request):
    return HttpResponse("Vista create_experiment")


def read_experiment(request, experiment):
    print "devolvemos edicion"
    d1 = {
        u'cpoints': [
            {u'lsb': u'00000001', u'freq_unit': u'hz', u't_unit': u'ns', u'type': u'C', u'msb': u'00000000', u'time': u'0', u'phase': u'0', u'freq': u'0', u'data': u'0', u'id': 1523141654228L},
            {u'lsb': u'00000001', u'freq_unit': u'hz', u't_unit': u'ns', u'type': u'L', u'msb': u'00000000', u'time': u'0', u'phase': u'0', u'freq': u'0', u'data': u'0', u'id': 1523141655342L},
            {u'lsb': u'00000001', u'freq_unit': u'hz', u't_unit': u'ns', u'type': u'C', u'msb': u'00000000', u'time': u'0', u'phase': u'0', u'freq': u'0', u'data': u'0', u'id': 1523141655519L},
            {u'lsb': u'00000001', u'freq_unit': u'hz', u't_unit': u'ns', u'type': u'R', u'msb': u'00000000', u'time': u'0', u'phase': u'0', u'freq': u'0', u'data': u'0', u'id': 1523141655697L},
            {u'lsb': u'00000001', u'freq_unit': u'hz', u't_unit': u'ns', u'type': u'C', u'msb': u'00000000', u'time': u'0', u'phase': u'0', u'freq': u'0', u'data': u'0', u'id': 1523141657471L},
            {u'lsb': u'00000001', u'freq_unit': u'hz', u't_unit': u'ns', u'type': u'L', u'msb': u'00000000', u'time': u'0', u'phase': u'0', u'freq': u'0', u'data': u'0', u'id': 1523141657632L},
            {u'lsb': u'00000001', u'freq_unit': u'hz', u't_unit': u'ns', u'type': u'C', u'msb': u'00000000', u'time': u'0', u'phase': u'0', u'freq': u'0', u'data': u'0', u'id': 1523141673163L},
            {u'lsb': u'00000001', u'freq_unit': u'hz', u't_unit': u'ns', u'type': u'R', u'msb': u'00000000', u'time': u'0', u'phase': u'0', u'freq': u'0', u'data': u'0', u'id': 1523141673328L}
        ],
        u'settings':
            {
            u'a_times': u'50',
            u'a_name': u'Experimento de pruebas',
            u'a_description': u'Este es un experimento de pruebas',
            u'a_freq': u'100',
            u'a_msb': u'10000001',
            u'a_freq_unit': u'mhz',
            u'a_ts_unit': u'us',
            u'a_lsb': u'10000001',
            u'a_ts': u'10',
            u'a_bloq': u'8'
            }
        }

    d2 = {"cpoints":[], "settings":{
            "a_times": "50",
            "a_name": "Experimento de pruebas",
            "a_description": "Este es un experimento de pruebas",
            "a_freq": "100",
            "a_msb": "10000001",
            "a_freq_unit": "mhz",
            "a_ts_unit": "us",
            "a_lsb": "10000001",
            "a_ts": "10",
            "a_bloq": "8"
            }
        }
    dd = { "authError": False,"error": False, "msg": "operacion realizada con exito", "data": d1}
    return dd


def update_experiment(request):
    return HttpResponse("Vista update_experiment")


def delete_experiment(request):
    return HttpResponse("Vista delete_experiment")


def list_experiment(request):
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
    return dd

@login_required
def experiment_switch(request, username, experiment):

    dd = {}

    if request.method == "POST":
        data = json.loads(request.body)
        pprint(data)
        dd = {"expId":33336666}

    if request.method == "GET":
        if experiment:
            dd = read_experiment(request, experiment)
            pprint("retornamos exp {}".format(experiment))
        else:
            dd = list_experiment(request)

    if request.method == "PATCH":
        data = json.loads(request.body)
        pprint(data)
        if data["execute"]:
            pprint("ejecutamos el experimento {}".format(data["settings"]))
            dd = {"expId":33336666}
        else:
            pprint("actualizamos el experimento {}".format(data["settings"]))

    if request.method == "DELETE":
        dd = {"m": "delete"}

    j = json.dumps(dd)

    return HttpResponse(j, content_type="application/json")
