from models import Result
from datetime import datetime
import json
import csv
import StringIO
import zipfile
import cStringIO
import codecs
import pytz
from pytz import country_timezones, timezone
from django.db import reset_queries, close_old_connections

def create_result(username, data):
    experiment = json.dumps(data)
    author = username
    date_time = datetime.now(pytz.timezone(country_timezones["AR"][1]))
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
    e.date_time = datetime.now(pytz.timezone(country_timezones["AR"][1]))
    e.data = json.dumps(d)
    e.save()
    # reset_queries()
    # close_old_connections()



def update_result_err(username, id, data):
    e = Result.objects.get(author=username, id=id)
    l = json.loads(e.error)
    l.append(data)
    e.error = json.dumps(l)
    e.save()


def update_result_log(username, id, data):
    e = Result.objects.get(author=username, id=id)
    e.date_time = datetime.now(pytz.timezone(country_timezones["AR"][1]))
    e.log = json.dumps(data)
    e.save()
    # reset_queries()
    # close_old_connections()


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


def acq_sum(l1, l2):
    assert len(l1) == len(l2)
    for i in xrange(len(l1)):
        l2[i][1] = l1[i][1] + l2[i][1]


def result_to_zip(username, id):
    e = Result.objects.get(author=username, id=id)

    data = json.loads(e.data)

    sio_buffer_values = []
    zip_buffer = StringIO.StringIO()
    zip = zipfile.ZipFile(zip_buffer, "w")

    acquisitions_channel_a = data["a"]
    if acquisitions_channel_a:
        c_acq_ch_a = [[i, 0] for i in xrange(len(acquisitions_channel_a[0]))]

        # no son requeridas las lecturas intermedias
        for acquisition in acquisitions_channel_a:
            acq_sum(acquisition, c_acq_ch_a)
        #     buffer = StringIO.StringIO()
        #     csv_out = csv.writer(buffer)
        #     csv_out.writerow(["x", "y"])
        #     for sample in acquisition:
        #         csv_out.writerow(sample)
        #     sio_buffer_values.append(buffer.getvalue())
        #
        # counter = 0
        # for sio_buffer_value in sio_buffer_values:
        #     zip.writestr("./report/channel_a/{}.csv".format(counter), sio_buffer_value)
        #     counter+=1

        # write acq sum for A
        sio_buffer_values = []
        buffer = StringIO.StringIO()
        csv_out = csv.writer(buffer)
        csv_out.writerow(["x", "y"])
        for sample in c_acq_ch_a:
            csv_out.writerow(sample)
        sio_buffer_values.append(buffer.getvalue())
        counter = 0
        for sio_buffer_value in sio_buffer_values:
            zip.writestr("./report/channel_a/total_{}.csv".format(counter), sio_buffer_value)
            counter += 1
    else:
        print "reporte canal A vacio"


    sio_buffer_values = []
    acquisitions_channel_b = data["b"]
    if acquisitions_channel_b:
        c_acq_ch_b = [[i, 0] for i in xrange(len(acquisitions_channel_b[0]))]

        # no son requeridas las lecturas intermedias
        for acquisition in acquisitions_channel_b:
            acq_sum(acquisition, c_acq_ch_b)
        #     buffer = StringIO.StringIO()
        #     csv_out = csv.writer(buffer)
        #     csv_out.writerow(["x", "y"])
        #     for sample in acquisition:
        #         csv_out.writerow(sample)
        #     sio_buffer_values.append(buffer.getvalue())
        #
        # counter = 0
        # for sio_buffer_value in sio_buffer_values:
        #     zip.writestr("./report/channel_b/{}.csv".format(counter), sio_buffer_value)
        #     counter += 1

        # write acq sum for B
        sio_buffer_values = []
        buffer = StringIO.StringIO()
        csv_out = csv.writer(buffer)
        csv_out.writerow(["x", "y"])
        for sample in c_acq_ch_b:
            csv_out.writerow(sample)
        sio_buffer_values.append(buffer.getvalue())
        counter = 0
        for sio_buffer_value in sio_buffer_values:
            zip.writestr("./report/channel_b/total_{}.csv".format(counter), sio_buffer_value)
            counter += 1
    else:
        print "reporte canal B vacio"

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
    cba = timezone(country_timezones["AR"][0])
    for result in results:
        d.append({
            "id": str(result.id),
            "created": result.date_time.astimezone(cba).strftime("%Y-%m-%d %H:%M:%S"),
            "author": result.author,
            "resume": result.resume,
            "state": result.status
        })

    dd = {"error": False, "msg": "tu consulta no esta permitida", "username": "jperez", "authError": False, "datas": d}
    return dd


def get_result_experiment_by_user_and_id(username, id):
    e = Result.objects.get(author=username, id=id)
    return e.experiment


def is_status_final(username, id):
    e = Result.objects.get(author=username, id=id)
    return not e.status == "running"