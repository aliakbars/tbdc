from wsgiref.util import FileWrapper
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from patient.models import *
from datetime import datetime, date
import json
import subprocess
import os

# Create your views here.
def index(request):
    return render(request, 'index.html')

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def patient_index(request):
    return render(request, 'patient/index.html')

def patient_show(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    patient.age = calculate_age(patient.birthdate)
    data = {
        'patient': patient,
        'lab_results': patient.labresult_set.all(),
        'treatments': patient.treatment_set.all(),
        'appointments': patient.appointment_set.filter(date__lt=date.today()),
        'upcoming_appt': patient.appointment_set.filter(date__gte=date.today()).order_by('date')[0]
    }
    return render(request, 'patient/show.html', data)

def appointment_create(request, patient_id):
    if request.method == 'POST':
        fields = ['service_type', 'agenda', 'date']
        empty_field = []
        for field in fields:
            if not request.POST.get(field, ''):
                empty_field.append(field)
        if empty_field:
            messages.error(request, 'Please fill out these fields: %s' % ', '.join(empty_field))
            print 'Please fill out these fields: %s' % ', '.join(empty_field)
        else:
            user = User.objects.get(id=1)
            patient = Patient.objects.get(id=patient_id)
            appointment = patient.appointment_set.create(
                service_type=request.POST['service_type'],
                agenda=request.POST['agenda'],
                date=request.POST['date'],
                creator=user
            )
            messages.success(request, 'Appointment scheduled.')
            return HttpResponseRedirect(reverse('patient.views.patient_show', args=(patient.id,)))
    patient = Patient.objects.get(id=patient_id)
    patient.age = calculate_age(patient.birthdate)
    return render(request, 'appointment/create.html', {'patient': patient})

def handle_api(request, obj):
    response_data = {}
    if request.method == 'GET':
        fields = ['patient_id']
        empty_field = []
        for field in fields:
            if not request.GET.get(field, ''):
                empty_field.append(field)
        if empty_field:
            response_data['status'] = 'error'
            response_data['message'] = 'You have not set the parameter for %s' % ', '.join(empty_field)
        else:
            data = obj.objects.filter(patient__identifier=request.GET['patient_id']) # filter(date_created__gte=datetime.today())
            response_data['status'] = 'success'
            response_data['message'] = list(data.values())

        return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), content_type='application/json')
    response_data['status'] = 'error'
    response_data['message'] = 'Method not allowed!'
    return HttpResponse(json.dumps(response_data), content_type='application/json')

def appointment_get(request):
    return handle_api(request, Appointment)

def treatment_get(request):
    return handle_api(request, Treatment)

def lab_result_afb_store(creator, filename):
    parameters = filename.split('_')
    identifier = parameters[-1].split('.')[0]
    patient = Patient.objects.get(identifier=identifier)
    if result == 0:
        result = 'MTB Negative'
    else:
        result = 'MTB Positive (%d)' % parameters[0]
    lab_result = LabResult(patient=patient, test_name='Microscopic AFB', img=filename, result=result, creator=creator)

def lab_result_create(request):
    return render(request, 'labresult/index.html')

@csrf_exempt
def lab_result_store(request):
    response_data = {}
    if request.method == 'POST':
        fields = ['username', 'password', 'patient_id']
        empty_field = []
        for field in fields:
            if not request.POST.get(field, ''):
                empty_field.append(field)
        if empty_field or 'photo' not in request.FILES:
            response_data['status'] = 'error'
            response_data['message'] = 'Please fill out these fields: %s' % ', '.join(empty_field)
        elif request.FILES['photo'].name.split('.')[-1].lower() not in ['jpg','jpeg']:
            response_data['status'] = 'error'
            response_data['message'] = 'Invalid file extension! (.jpg needed)'
        else:
            user = authenticate(username=request.POST.get('username',''), password=request.POST.get('password',''))
            if user is not None:
                filename = handle_upload(request, field_name='photo')
                extension = filename.split('.')[-1]
                response_data['status'] = 'success'
                response_data['message'] = 'Photo uploaded!'
                # subprocess.Popen('') # Input script here
                # filenames = os.listdir(settings.MEDIA_ROOT + 'result')
                # for f in filenames:
                #     # Process file here
                #     break
            else:
                response_data['status'] = 'error'
                response_data['message'] = 'Invalid username or password!'

        return HttpResponse(json.dumps(response_data), content_type='application/json')
    response_data['status'] = 'error'
    response_data['message'] = 'Method not allowed!'
    return HttpResponse(json.dumps(response_data), content_type='application/json')

def handle_upload(request, field_name):
    today = datetime.today()
    extension = request.FILES[field_name].name.split('.')[-1]
    filename = settings.MEDIA_ROOT + today.strftime("%y%m%d_%H%M%S") + '_' + request.POST.get('patient_id','') + '.' + extension
    with open(filename, 'wb+') as dest:
        for chunk in request.FILES[field_name].chunks():
            dest.write(chunk)
        return filename