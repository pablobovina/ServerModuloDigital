from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<username>.+)/logout', views.logout_user),
    url(r'^(?P<username>.+)', views.log_user),
]
