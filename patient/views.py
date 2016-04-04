from wsgiref.util import FileWrapper
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from patient.models import *
from datetime import datetime, date
import json
import subprocess
import os

def generateID():
    return ''.join(random.sample(set(string.letters.upper()), 3) + random.sample(string.digits, 5))

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def patient_get(request):
    response_data = {}
    if request.method == 'GET':
        if not request.GET.get('query', ''):
            response_data['status'] = 'success'
            response_data['message'] = Patient.objects.all()
        else:
            query = request.GET['query']
            data = Patient.objects.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(identifier__icontains=query)
            )
            response_data['status'] = 'success'
            response_data['message'] = list(data.values())

        return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), content_type='application/json')
    response_data['status'] = 'error'
    response_data['message'] = 'Method not allowed!'
    return HttpResponse(json.dumps(response_data), content_type='application/json')

def patient_index(request):
    return render(request, 'patient/index.html', {'query': request.GET.get('query', '')})

def patient_create(request):
    if request.method == 'POST':
        fields = ['first_name', 'last_name', 'birthdate', 'address', 'city', 'province', 'country', 'phone_number']
        empty_field = []
        for field in fields:
            if not request.POST.get(field, ''):
                empty_field.append(field)
        if empty_field:
            messages.error(request, 'Please fill out these fields: %s' % ', '.join(empty_field))
        else:
            identifier = generateID()
            user = User.objects.create_user(identifier, password=identifier,
                first_name=request.POST['first_name'], last_name=request.POST['last_name'])
            patient = user.patient_set.create(
                identifier=identifier,
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                birthdate=request.POST['birthdate'],
                address=request.POST['address'],
                city=request.POST['city'],
                province=request.POST['province'],
                country=request.POST['country'],
                phone_number=request.POST['phone_number']
            )
            patient.save()
            return HttpResponseRedirect(reverse('patient.views.patient_show', args=(patient.id,)))
    data = {}
    name = request.GET.get('name', '').split(' ')
    if name:
        data['first_name'] = ' '.join(name[:-1])
        data['last_name'] = name[-1]
    data['birthdate'] = request.GET.get('birthdate', '')
    data['gender'] = request.GET.get('gender', '')
    return render(request, 'patient/create.html', {'data': data})

def patient_show(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    patient.age = calculate_age(patient.birthdate)
    visits = patient.visit_set.order_by('-date_created')
    if visits:
        last_visit = visits[0]
    else:
        last_visit = None
    vitals = patient.vitals_set.order_by('-date_created')
    if vitals:
        vitals = vitals[0]
    upcoming = patient.appointment_set.filter(date__gte=date.today()).order_by('date')
    if upcoming:
        upcoming = upcoming[0]
    data = {
        'patient': patient,
        'lab_results': patient.labresult_set.all(),
        'treatments': patient.treatment_set.all(),
        'appointments': patient.appointment_set.filter(date__lt=date.today()),
        'visits': visits,
        'last_visit': last_visit,
        'vitals': vitals,
        'upcoming_appt': upcoming
    }
    return render(request, 'patient/show.html', data)

def screening_create(request, patient_id):
    if request.method == 'POST':
        fields = [
            'diagnosis',
            'hiv',
            'tb_exposure'
        ]
        empty_field = []
        for field in fields:
            if not request.POST.get(field, ''):
                empty_field.append(field)
        if empty_field:
            messages.error(request, 'Please fill out these fields: %s' % ', '.join(empty_field))
        else:
            user = User.objects.get(id=1)
            patient = Patient.objects.get(id=patient_id)
            screening = patient.screening_set.create(
                cough = request.POST.get('cough', False),
                haemoptysis = request.POST.get('haemoptysis', False),
                chest_pain = request.POST.get('chest_pain', False),
                weight_loss = request.POST.get('weight_loss', False),
                fatigue = request.POST.get('fatigue', False),
                fever = request.POST.get('fever', False),
                night_sweats = request.POST.get('night_sweats', False),
                chills = request.POST.get('chills', False),
                other_symptoms = request.POST.get('other_symptoms', False),
                diagnosis = request.POST.get('diagnosis', ''),
                tb_patient_status = request.POST.get('tb_patient_status', 0),
                meningitis = request.POST.get('meningitis', False),
                pregnant = request.POST.get('pregnant', False),
                immunocompromised = request.POST.get('immunocompromised', False),
                malnutrition = request.POST.get('malnutrition', False),
                coinfection = request.POST.get('coinfection', False),
                comorbid = request.POST.get('comorbid', False),
                hiv = request.POST['hiv'],
                tb_exposure = request.POST['tb_exposure'],
                creator = user
            )
            messages.success(request, 'TB screening form recorded.')
            return HttpResponseRedirect(reverse('patient.views.patient_show', args=(patient.id,)))
    patient = Patient.objects.get(id=patient_id)
    patient.age = calculate_age(patient.birthdate)
    return render(request, 'screening/create.html', {'patient': patient})

def visit_create(request, patient_id):
    if request.method == 'POST':
        fields = ['diagnoses', 'notes']
        empty_field = []
        for field in fields:
            if not request.POST.get(field, ''):
                empty_field.append(field)
        if empty_field:
            messages.error(request, 'Please fill out these fields: %s' % ', '.join(empty_field))
        else:
            user = User.objects.get(id=1)
            patient = Patient.objects.get(id=patient_id)
            visit = patient.visit_set.create(
                diagnoses=request.POST['diagnoses'],
                notes=request.POST['notes'],
                creator=user
            )
            messages.success(request, 'Visit notes recorded.')
            return HttpResponseRedirect(reverse('patient.views.patient_show', args=(patient.id,)))
    patient = Patient.objects.get(id=patient_id)
    patient.age = calculate_age(patient.birthdate)
    return render(request, 'visit/create.html', {'patient': patient})

def vitals_create(request, patient_id):
    if request.method == 'POST':
        fields = ['height', 'weight', 'temperature', 'pulse', 'respiratory_rate', 'bp_systole', 'bp_diastole']
        empty_field = []
        for field in fields:
            if not request.POST.get(field, ''):
                empty_field.append(field)
        if empty_field:
            messages.error(request, 'Please fill out these fields: %s' % ', '.join(empty_field))
        else:
            user = User.objects.get(id=1)
            patient = Patient.objects.get(id=patient_id)
            vitals = patient.vitals_set.create(
                height=request.POST['height'],
                weight=request.POST['weight'],
                temperature=request.POST['temperature'],
                pulse=request.POST['pulse'],
                respiratory_rate=request.POST['respiratory_rate'],
                bp_systole=request.POST['bp_systole'],
                bp_diastole=request.POST['bp_diastole'],
                creator=user
            )
            messages.success(request, 'Vitals recorded.')
            return HttpResponseRedirect(reverse('patient.views.patient_show', args=(patient.id,)))
    patient = Patient.objects.get(id=patient_id)
    patient.age = calculate_age(patient.birthdate)
    return render(request, 'vitals/create.html', {'patient': patient})

def vitals_trend(request, patient_id, column):
    patient = Patient.objects.get(id=patient_id)
    patient.age = calculate_age(patient.birthdate)
    vitals = patient.vitals_set.order_by('date_created')
    labels = '"%s"' % ','.join([v.date_created.strftime('%Y-%m-%d') for v in vitals])
    data = ','.join([str(v) for v in vitals.values_list(column, flat=True)])
    column_name = column.replace('_', ' ').title()
    return render(request, 'vitals/trend.html', {'patient': patient, 'labels': labels, 'data': data, 'column_name': column_name})

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

@login_required
def treatment_create(request, patient_id):
    if request.method == 'POST':
        fields = ['medication', 'dosage', 'freq_day', 'freq_week', 'start_date', 'end_date']
        empty_field = []
        for field in fields:
            if not request.POST.getlist(field, ''):
                print request.POST.getlist(field)
                empty_field.append(field)
        if empty_field:
            messages.error(request, 'Please fill out these fields: %s' % ', '.join(empty_field))
        else:
            user = User.objects.get(id=1)
            patient = Patient.objects.get(id=patient_id)
            medications = request.POST.getlist('medication')
            dosages = request.POST.getlist('dosage')
            freq_days = request.POST.getlist('freq_day')
            freq_weeks = request.POST.getlist('freq_week')
            start_dates = request.POST.getlist('start_date')
            end_dates = request.POST.getlist('end_date')
            for i in range(len(request.POST.getlist('medication'))):
                treatment = patient.vitals_set.create(
                    medication=medications[i],
                    dosage=dosages[i],
                    freq_day=freq_days[i],
                    freq_week=freq_weeks[i],
                    start_date=start_dates[i],
                    end_date=end_dates[i],
                    creator=user
                )
            messages.success(request, 'Medications added.')
            return HttpResponseRedirect(reverse('patient.views.patient_show', args=(patient.id,)))
    patient = Patient.objects.get(id=patient_id)
    patient.age = calculate_age(patient.birthdate)
    return render(request, 'treatment/create.html', {'patient': patient})

def treatment_show(request, patient_id):
    pass

def treatment_get(request):
    return handle_api(request, Treatment)

def lab_result_afb_store(creator, filename):
    parameters = filename.split('_')
    result = int(parameters[0])
    identifier = parameters[-1].split('.')[0]
    patient = Patient.objects.get(identifier=identifier)
    if result == 0:
        result = 'MTB Negative'
    else:
        result = 'MTB Positive (%d)' % int(parameters[0])
    lab_result = LabResult(patient=patient, test_name='Microscopic AFB', img=filename, result=result, creator=creator)
    lab_result.save()

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
                from random import randint
                from shutil import copyfile
                bacillus = randint(0,5)
                copyfile(settings.MEDIA_ROOT + filename, settings.MEDIA_ROOT + 'result/' + str(bacillus) + '_' + filename)
                # subprocess.Popen('') # Input script here
                filenames = os.listdir(settings.MEDIA_ROOT + 'result')
                for f in filenames:
                    lab_result_afb_store(user, f)
            else:
                response_data['status'] = 'error'
                response_data['message'] = 'Invalid username or password!'

        return HttpResponse(json.dumps(response_data), content_type='application/json')
    response_data['status'] = 'error'
    response_data['message'] = 'Method not allowed!'
    return HttpResponse(json.dumps(response_data), content_type='application/json')

def lab_result_show(request, patient_id, lab_result_id):
    patient = Patient.objects.get(id=patient_id)
    patient.age = calculate_age(patient.birthdate)
    lab_result = LabResult.objects.get(id=lab_result_id)
    user = lab_result.creator
    return render(request, 'labresult/show.html', {'patient': patient, 'lab_result': lab_result, 'user': user})

def handle_upload(request, field_name):
    today = datetime.today()
    extension = request.FILES[field_name].name.split('.')[-1]
    filename = today.strftime("%y%m%d_%H%M%S") + '_' + request.POST.get('patient_id','') + '.' + extension
    with open(settings.MEDIA_ROOT + filename, 'wb+') as dest:
        for chunk in request.FILES[field_name].chunks():
            dest.write(chunk)
        return filename