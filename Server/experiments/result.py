from models import Result
from datetime import datetime
import json
import csv
import StringIO
import zipfile
import cStringIO
import codecs


def create_result(username, data):
    experiment = json.dumps(data)
    author = username
    date_time = datetime.now()
    resume = json.loads(experiment)["settings"]["a_description"]
    status = "partial"
    e = Result(author=author, experiment=experiment, date_time=date_time, resume=resume, status=status,
               error=json.dumps([]), log="", data=json.dumps({"a": [], "b": []}))
    e.save()
    return e.id


def update_result_data(username, id, data):
    e = Result.objects.get(author=username, id=id)
    d = json.loads(e.data)
    d["a"].append(data[0])
    d["b"].append(data[1])
    e.date_time = datetime.now()
    e.data = json.dumps(d)
    e.save()


def update_result_err(username, id, data):
    e = Result.objects.get(author=username, id=id)
    l = json.loads(e.error)
    l.append(data)
    e.error = json.dumps(l)
    e.save()


def update_result_log(username, id, data):
    e = Result.objects.get(author=username, id=id)
    e.date_time = datetime.now()
    e.log = json.dumps(data)
    e.save()


def update_result_status_finish(username, id):
    e = Result.objects.get(author=username, id=id)
    e.status = "finished"
    e.save()


def update_result_status_running(username, id):
    e = Result.objects.get(author=username, id=id)
    e.status = "running"
    e.save()


def update_result_status_error(username, id):
    print username, id
    e = Result.objects.get(author=username, id=id)
    e.status = "error"
    e.save()


def update_result_status_stop(username, id):
    print username, id
    e = Result.objects.get(author=username, id=id)
    e.status = "stopped"
    e.save()


def result_to_zip(username, id):
    e = Result.objects.get(author=username, id=id)

    data = json.loads(e.data)

    sio_buffer_values = []
    zip_buffer = StringIO.StringIO()
    zip = zipfile.ZipFile(zip_buffer, "w")

    acquisitions_channel_a = data["a"]
    for acquisition in acquisitions_channel_a:
        buffer = StringIO.StringIO()
        csv_out = csv.writer(buffer)
        csv_out.writerow(["x", "y"])
        for sample in acquisition:
            csv_out.writerow(sample)
        sio_buffer_values.append(buffer.getvalue())

    counter = 0
    for sio_buffer_value in sio_buffer_values:
        zip.writestr("./report/channel_a/{}.csv".format(counter), sio_buffer_value)
        counter+=1

    sio_buffer_values = []
    acquisitions_channel_b = data["b"]
    for acquisition in acquisitions_channel_b:
        buffer = StringIO.StringIO()
        csv_out = csv.writer(buffer)
        csv_out.writerow(["x", "y"])
        for sample in acquisition:
            csv_out.writerow(sample)
        sio_buffer_values.append(buffer.getvalue())

    counter = 0
    for sio_buffer_value in sio_buffer_values:
        zip.writestr("./report/channel_b/{}.csv".format(counter), sio_buffer_value)
        counter += 1

    codecinfo = codecs.lookup("utf8")

    log = cStringIO.StringIO()
    log_wrapper = codecs.StreamReaderWriter(log, codecinfo.streamreader, codecinfo.streamwriter)
    log_wrapper.writelines(json.loads(e.log))
    zip.writestr("./report/log.txt", log.getvalue())

    err = cStringIO.StringIO()
    err_wrapper = codecs.StreamReaderWriter(err, codecinfo.streamreader, codecinfo.streamwriter)
    err_wrapper.writelines(json.loads(e.error))
    zip.writestr("./report/err.txt", err.getvalue())

    exp = cStringIO.StringIO()
    exp_wrapper = codecs.StreamReaderWriter(exp, codecinfo.streamreader, codecinfo.streamwriter)
    exp_wrapper.write(e.experiment)
    zip.writestr("./report/experiment.json", exp.getvalue())

    zip.close()
    return zip_buffer.getvalue()


def result_by_user(username):
    d = []
    results = Result.objects.filter(author=username)
    for result in results:
        d.append({
            "id": str(result.id),
            "created": result.date_time.strftime("%Y-%m-%d %H:%M:%S"),
            "author": result.author,
            "resume": result.resume,
            "state": result.status
        })

    dd = {"error": False, "msg": "tu consulta no esta permitida", "username": "jperez", "authError": False, "datas": d}
    return dd


def get_result_experiment_by_user_and_id(username, id):
    e = Result.objects.get(author=username, id=id)
    return e.experiment