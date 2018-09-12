# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from experiment import create_experiment, read_experiment, list_experiment, delete_experiment, update_experiment
from result_manager_thread import *
from manager_thread import create_manager_thread, get_pid_name_by_result_id
from result import create_result, result_by_user, result_to_zip, get_result_experiment_by_user_and_id
import json


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
        update_experiment(u, int(id), request.body)

    if request.method == "DELETE":
        delete_experiment(u, int(id))

    return HttpResponse(json.dumps(res), content_type="application/json")


@login_required
def run_experiment(request, username, id):
    u = request.user
    data = json.loads(read_experiment(u, int(id)))
    id_result = create_result(username, data)
    id_thread = create_manager_thread(username, id_result)
    mgr = ResultManagerThread()
    mgr.new_thread(u, int(id), id_result, id_thread, data)
    mgr.on_start()
    return HttpResponse(json.dumps({"expId": id, "expIdRes": id_result}))


@login_required
def stop_result(request, username, id):
    pid, name = get_pid_name_by_result_id(request.user, int(id))
    mgr = ResultManagerThread()
    mgr.stop_thread(pid, name)
    return HttpResponse(json.dumps({"pid": pid, "name": name}))


@login_required
def list_result(request, username):
    return HttpResponse(json.dumps(result_by_user(request.user)), content_type="application/json")


@login_required
def get_result_experiment(request, username, id):
    experiment = get_result_experiment_by_user_and_id(request.user, int(id))
    res = {"data": json.loads(experiment)}
    return HttpResponse(json.dumps(res), content_type="application/json")


@login_required
def zip_result(request, username, id):
    return HttpResponse(result_to_zip(username, int(id)), content_type="application/zip")


