# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate, login, logout


def log_user(request, username):

    print request
    data = json.loads(request.body)
    u = data["user"]
    p = data["pass"]

    user = authenticate(username=u, password=p)

    if user is not None:
        login(request, user)
        return HttpResponse("login success for {}".format(u))

    return HttpResponse(json.dumps({"error": 'usuario "{}" no autenticado'.format(u)}), status=500)


def logout_user(request, username):
    logout(request)
    return HttpResponse("logout success for {}".format(username))
