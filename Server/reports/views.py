# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from random import uniform
import json
import shutil


def get_report(request, username, experiment):
    j = json.dumps([{"x": i, "y": uniform(0, 1)} for i in xrange(0,10)])
    return HttpResponse(j, content_type="application/json")


def get_zip(request, username, experiment):
    zip_file = shutil.make_archive("./zip/resultado", "zip", "./out")
    return HttpResponse(open("./zip/resultado.zip", 'rb'), content_type="application/zip")
