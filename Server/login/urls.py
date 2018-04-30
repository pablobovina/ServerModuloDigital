from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<username>.+)/', views.log_user),
]