from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<experiment>.+)?/run', views.run_experiment),
    url(r'^stop', views.stop_experiment),
    url(r'^status', views.status_experiment),
    url(r'^queuerun', views.run_queue_experiment)
]
