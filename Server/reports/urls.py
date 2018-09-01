from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^rep', views.get_report),
    url(r'^zip', views.get_zip),
]