from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.patient_index, name='index'),
    url(r'^(\d+)/$', views.patient_show),
    url(r'^get$', views.patient_get),
    url(r'^create$', views.patient_create),
    url(r'^(\d+)/appointment/create$', views.appointment_create),
    url(r'^(\d+)/appointment/(\d+)$', views.appointment_show),
    url(r'^appointment/get$', views.appointment_get),
    url(r'^lab_result/create$', views.lab_result_create),
    url(r'^lab_result/store$', views.lab_result_store),
    url(r'^(\d+)/lab_result/(\d+)$', views.lab_result_show),
    url(r'^(\d+)/visit/create$', views.visit_create),
    url(r'^(\d+)/vitals/create$', views.vitals_create),
    url(r'^(\d+)/vitals/trend/(\w+)$', views.vitals_trend),
    url(r'^(\d+)/screening/create$', views.screening_create),
    url(r'^(\d+)/screening/(\d+)$', views.screening_show),
    url(r'^(\d+)/treatment/create$', views.treatment_create),
    url(r'^treatment/get$', views.treatment_get),
]