# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from models import Experiment
from datetime import datetime
import json


def create_experiment(username, experiment):
    author = username
    date_time = datetime.now()
    resume = json.loads(experiment)["settings"]["a_description"]
    status = "created"
    e = Experiment(author=author, experiment=experiment, date_time=date_time, resume=resume, status=status)
    e.save()
    return e.id


def read_experiment(username, id):
    e = Experiment.objects.get(author=username, id=id)
    if e.experiment:
        return e.experiment
    return False


def update_experiment(username, id, experiment):
    try:
        e = Experiment.objects.get(author=username, id=id)
        e.experiment = experiment
        e.date_time = datetime.now()
        e.resume = json.loads(experiment)["settings"]["a_description"]
        e.status = "created"
        e.save()
        return id
    except Exception as ex:
        print ex.message
        return False


def delete_experiment(username, id):
    try:
        Experiment.objects.get(author=username, id=id).delete()
        return True
    except Exception as e:
        print e.message
        return False


def list_experiment(username):
    d = []
    experiments = Experiment.objects.filter(author=username)
    for experiment in experiments:
        d.append({
            "id": str(experiment.id),
            "created": experiment.date_time.strftime("%Y-%m-%d %H:%M:%S"),
            "author": experiment.author,
            "resume": experiment.resume,
            "state": experiment.status
        })

    dd = {"error": False, "msg": "tu consulta no esta permitida", "username": "jperez", "authError": False, "datas": d}
    return dd


@login_required
def experiment_switch(request, username, id):

    u = request.user
    res = {}

    if request.method == "POST":
        res = create_experiment(u, request.body)
        res = {"expId": res}

    if request.method == "GET":
        if id:
            res = read_experiment(u, int(id))
            res = {"data": json.loads(res)}
        else:
            res = list_experiment(u)

    if request.method == "PATCH":
        res = update_experiment(u, int(id), request.body)

    if request.method == "DELETE":
        res = delete_experiment(u, int(id))

    return HttpResponse(json.dumps(res), content_type="application/json")
