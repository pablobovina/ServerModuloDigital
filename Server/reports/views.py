# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse


def get_report(request):
    return HttpResponse("Vista reporte generado")
