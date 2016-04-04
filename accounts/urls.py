from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.auth),
    url(r'^logout/$', views.signout),
]