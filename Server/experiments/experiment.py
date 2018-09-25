from datetime import datetime
from models import Experiment
import json
import pytz
from pytz import country_timezones, timezone


def create_experiment(username, experiment):
    author = username
    date_time = datetime.now(pytz.timezone(country_timezones["AR"][1]))
    resume = json.loads(experiment)["settings"]["a_description"]
    status = "created"
    e = Experiment(author=author, experiment=experiment, date_time=date_time, resume=resume, status=status)
    e.save()
    return e.id


def read_experiment(username, id):
    e = Experiment.objects.get(author=username, id=id)
    return e.experiment


def update_experiment(username, id, experiment):
    e = Experiment.objects.get(author=username, id=id)
    e.experiment = experiment
    e.date_time = datetime.now(pytz.timezone(country_timezones["AR"][1]))
    e.resume = json.loads(experiment)["settings"]["a_description"]
    e.status = "created"
    e.save()


def delete_experiment(username, id):
    Experiment.objects.get(author=username, id=id).delete()


def list_experiment(username):
    d = []
    experiments = Experiment.objects.filter(author=username)
    cba = timezone(country_timezones["AR"][0])
    for experiment in experiments:
        d.append({
            "id": str(experiment.id),
            "created": experiment.date_time.astimezone(cba).strftime("%Y-%m-%d %H:%M:%S"),
            "author": experiment.author,
            "resume": experiment.resume,
            "state": experiment.status
        })

    dd = {"error": False, "msg": "tu consulta no esta permitida", "username": "jperez", "authError": False, "datas": d}
    return dd