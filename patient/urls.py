from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.patient_index, name='index'),
    url(r'^(\d+)/$', views.patient_show),
    url(r'^create$', views.patient_create),
    url(r'^appointment/(\d+)/create$', views.appointment_create),
    url(r'^appointment/get$', views.appointment_get),
    url(r'^lab_result/create$', views.lab_result_create),
    url(r'^lab_result/store$', views.lab_result_store),
    url(r'^(\d+)/lab_result/(\d+)$', views.lab_result_show),
    url(r'^treatment/get$', views.treatment_get),
]