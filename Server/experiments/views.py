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

experiments = {}
counter = 0


def create_experiment(request, username):
    global counter
    global experiments

    if username not in experiments.keys():
        experiments[username] = {}

    experiments[username][counter] = json.loads(request.body)
    res = counter
    counter += 1

    request.session["experiments"] = experiments
    request.session["counter"] = counter
    return res


def read_experiment(request, username, experiment):
    global experiments
    if username not in experiments.keys():
        return False
    if experiment not in experiments[username].keys():
        return False
    else:
        return experiments[username][experiment]


def update_experiment(request, username, experiment):
    global experiments
    if username not in experiments.keys():
        return False
    if experiment not in experiments[username].keys():
        return False
    else:
        experiments[username][experiment] = json.loads(request.body)

    request.session["experiments"] = experiments
    return True


def delete_experiment(request, username, experiment):
    global experiments
    if username not in experiments.keys():
        return False
    if experiment not in experiments[username].keys():
        return False
    else:
        del(experiments[username][experiment])

    request.session["experiments"] = experiments
    return True


def list_experiment(request):
    global experiments
    d = []
    # for i in range(n_users):
    #     d.append({"id": str(uuid.uuid4()),
    #               "created": [x for x in random_date(startDate, 1)][0].strftime("%c"),
    #               "author": choice(authors),
    #               "resume": choice(descr),
    #               "state": choice(states)})

    for author in experiments:
        for experiment in experiments[author]:
            d.append({
                "id": str(experiment),
                "created": "10/11/1988 20:30:34",
                "author": author,
                "resume": experiments[author][experiment]["settings"]["a_name"],
                "state": "creado"
            })

    dd = {"error": False, "msg": "tu consulta no esta permitida", "username": "jperez", "authError": False, "datas": d}
    return dd


# @login_required
def experiment_switch(request, username, experiment):

    res = {}
    if request.method == "POST":
        res = create_experiment(request, username)
        res = {"expId": res}
    if request.method == "GET":
        if experiment:
            res = read_experiment(request, username, int(experiment))
            res = {"data": res}
        else:
            res = list_experiment(request)

    if request.method == "PATCH":
        res = update_experiment(request, username, int(experiment))

    if request.method == "DELETE":
        res = delete_experiment(request, username, int(experiment))

    return HttpResponse(json.dumps(res), content_type="application/json")
