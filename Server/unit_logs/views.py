# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse


def dds2_log(request):
    return HttpResponse("Vista dds2_log")


def ad_log(request):
    return HttpResponse("Vista ad_log")


def pp2_log(request):
    return HttpResponse("Vista pp2_log")


def general_log(request):
    return HttpResponse("Vista general_log")
