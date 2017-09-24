from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^dds2', views.dds2_log),
    url(r'^ad', views.ad_log),
    url(r'^pp2', views.pp2_log),
    url(r'^general', views.general_log)
]