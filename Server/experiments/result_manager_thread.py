from ModuloDigital.main import ModDig
from ModuloDigital.dry_run import DryRun
from manager_thread import bind_manager_thread, finish_manager_thread, filter_running, update_killer
from result import update_result_status_running, \
                update_result_status_error, \
                update_result_log, \
                update_result_data, \
                update_result_err, \
                update_result_status_finish, \
                update_result_status_stop
import threading
from os.path import join

class ResultManagerThread(object):
    data = None
    out_d = None
    log_d = None
    error_d = None
    id_experiment = None
    user = None
    id_result = None
    id_thread = None
    pid = None
    mod_dig = None
    kill_event = None
    name = None
    stop = None
    killer = None

    def new_thread(self, user, id_experiment, id_result, id_thread, data):
        self.user = user
        self.data = data
        self.out_d = join(".", "out", user)
        self.log_d = join(".", "log", user)
        self.error_d = join(".", "error", user)
        self.id_experiment = id_experiment
        self.id_result = id_result
        self.id_thread = id_thread
        self.mod_dig = ModDig(parent=self)
        return self.mod_dig

    def on_start(self):
        # check hilos corriendo
        self.mod_dig.start()
        self.pid = self.mod_dig.ident
        self.name = self.mod_dig.getName()
        update_result_status_running(self.user, self.id_result)
        bind_manager_thread(self.user, self.id_thread, self.pid, self.name)

    def on_partial(self, exp):
        update_result_data(self.user, self.id_result, exp)

    def on_error(self, err, log_lines):
        # validar que termino y actualizar el estado en la BD
        update_result_status_error(self.user, self.id_result)
        update_result_err(self.user, self.id_result, err)
        update_result_log(self.user, self.id_result, log_lines)
        finish_manager_thread(self.user, self.id_thread, self.pid)

    def on_log(self, log_lines):
        update_result_log(self.user, self.id_result, log_lines)

    def on_finish(self, log_lines):
        # validar que termino y actualizar el estado en la BD
        update_result_status_finish(self.user, self.id_result)
        update_result_log(self.user, self.id_result, log_lines)
        finish_manager_thread(self.user, self.id_thread, self.pid)

    def stop_thread(self, ident, name):
        for t in threading.enumerate():
            if t.ident == ident:
                t.terminate_now = True
                self.stop = True
                break

    def on_stop(self, err, log_lines):
        update_result_status_stop(self.user, self.id_result)
        update_result_err(self.user, self.id_result, err)
        update_result_log(self.user, self.id_result, log_lines)
        finish_manager_thread(self.user, self.id_thread, self.pid)

    def kill_all(self, user):
        t_list = filter_running()
        res = []
        t_all = threading.enumerate()
        for t in t_list:
            for tt in t_all:
                if tt.ident == t.pid:
                    tt.terminate_now = True
                    update_killer(user, t.id)
                    res.append([t.pid, t.author, user])
        self.killer = res
        return res

    def new_dry_run(self, user, data):
        self.user = user
        self.data = data
        self.out_d = join(".", "out", user)
        self.log_d = join(".", "log", user)
        self.error_d = join(".", "error", user)
        self.mod_dig = DryRun(parent=self).run()
        return True
