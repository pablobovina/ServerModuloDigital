# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from random import uniform
import json

def get_report(request):
    j = json.dumps([{"x": i, "y": uniform(0, 1)} for i in xrange(0,10)])
    return HttpResponse(j, content_type="application/json")
