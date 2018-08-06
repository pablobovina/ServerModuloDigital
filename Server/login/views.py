# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate, login


def log_user(request, username):

    print request
    data = json.loads(request.body)
    u = data["user"]
    p = data["pass"]

    user = authenticate(username=u, password=p)

    if user is not None:
        login(request, user)
        return HttpResponse("{} {} ".format(u, p))

    return HttpResponse("usuario no autenticado {} {} {}".format(user, u, p))


def logout_user(request, username):
    return HttpResponse("nos vemos {}".format(username))
