# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from experiment import create_experiment, read_experiment, list_experiment, delete_experiment, update_experiment
from result_manager_thread import ResultManagerThread
from manager_thread import create_manager_thread, get_pid_name_by_result_id, filter_running
from result import create_result, result_by_user, result_to_zip, get_result_experiment_by_user_and_id, is_status_final
import json


@login_required
def experiment_switch(request, username, id):
    try:
        res = {}
        if request.method == "POST":
            res = create_experiment(username, request.body)
            res = {"expId": res}
        if request.method == "GET":
            if id:
                res = read_experiment(username, int(id))
                res = {"data": json.loads(res)}
            else:
                res = list_experiment(username)
        if request.method == "PATCH":
            update_experiment(username, int(id), request.body)
        if request.method == "DELETE":
            delete_experiment(username, int(id))
        return HttpResponse(json.dumps(res), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({"error": e.message}),
                            status=500,
                            content_type="application/json")


@login_required
def run_experiment(request, username, id):
    if len(filter_running()):
        return HttpResponse(json.dumps({"error": "hay un experimento corriendo cancelarlos para continuar"}),
                            status=500,
                            content_type="application/json")
    try:
        data = json.loads(read_experiment(username, int(id)))
        mgr = ResultManagerThread()
        mgr.clean_dirs(username)
        mgr.make_dirs(username)
        # dry - run
        mgr.new_dry_run(username, data)
        # real - run with new data because previous is dirty
        mgr.clean_dirs(username)
        mgr.make_dirs(username)
        data = json.loads(read_experiment(username, int(id)))
        id_result = create_result(username, data)
        id_thread = create_manager_thread(username, id_result)
        mgr.new_thread(username, int(id), id_result, id_thread, data)
        mgr.on_start()
        return HttpResponse(json.dumps({"expId": id, "expIdRes": id_result}))
    except Exception as e:
        return HttpResponse(json.dumps({"error": e.message}),
                            status=500,
                            content_type="application/json")


@login_required
def stop_result(request, username, id):
    if is_status_final(username, id):
        return HttpResponse(json.dumps({"error": "experimento finalizado"}),
                            status=500,
                            content_type="application/json")
    try:
        pid, name = get_pid_name_by_result_id(username, int(id))
        mgr = ResultManagerThread()
        mgr.stop_thread(pid, name)
        return HttpResponse(json.dumps({"pid": pid, "name": name}))
    except Exception as e:
        return HttpResponse(json.dumps({"error": e.message}),
                            status=500,
                            content_type="application/json")


@login_required
def list_result(request, username):
    return HttpResponse(json.dumps(result_by_user(username)), content_type="application/json")


@login_required
def get_result_experiment(request, username, id):
    experiment = get_result_experiment_by_user_and_id(username, int(id))
    res = {"data": json.loads(experiment)}
    return HttpResponse(json.dumps(res), content_type="application/json")


@login_required
def zip_result(request, username, id):
    return HttpResponse(result_to_zip(username, int(id)), content_type="application/zip")


@login_required
def stop_all(request, username):
    if not len(filter_running()):
        return HttpResponse(json.dumps({"error": "no hay experiementos en ejecucion"}),
                            status=500,
                            content_type="application/json")
    try:
        mgr = ResultManagerThread()
        res = mgr.kill_all(username)
        return HttpResponse(json.dumps(res), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({"error": e.message}),
                            status=500,
                            content_type="application/json")
