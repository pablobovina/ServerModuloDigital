from models import ManagerThread
from datetime import datetime


def create_manager_thread(username, id_result):
    pid = -1
    running = True
    author = username
    date_time = datetime.now()
    e = ManagerThread(pid=pid, running=running, author=author, date_time=date_time, id_result=id_result)
    e.save()
    return e.id


def bind_manager_thread(username, id, pid, name):
    e = ManagerThread.objects.get(author=username, id=id)
    e.pid = pid
    e.name = name
    e.save()
    return e.id


def finish_manager_thread(username, id, pid):
    print username, id, pid
    e = ManagerThread.objects.get(author=username, id=id)
    e.running = False
    e.save()
    return e.id


def get_pid_name_by_result_id(username, id_result):
    e = ManagerThread.objects.get(author=username, id_result=id_result)
    return e.pid, e.name