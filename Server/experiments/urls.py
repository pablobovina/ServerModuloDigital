from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'results', views.list_result),
    url(r'(?P<id>.+)?/run', views.run_experiment),
    url(r'(?P<id>.+)?/stop', views.stop_result),
    url(r'(?P<id>.+)?/result_experiment', views.get_result_experiment),
    url(r'(?P<id>.+)?/zip', views.zip_result),
    url(r'(?P<id>.+)?', views.experiment_switch)
]
