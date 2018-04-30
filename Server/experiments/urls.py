from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^create', views.create_experiment),
    url(r'^read', views.read_experiment),
    url(r'^update', views.update_experiment),
    url(r'^delete', views.delete_experiment),
    url(r'(?P<experiment>.+)?', views.experiment_switch),
]