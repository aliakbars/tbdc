from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import random, string

# Create your models here.
class Patient(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    identifier = models.CharField(max_length=255)
    first_name = models.CharField(max_length=127)
    last_name = models.CharField(max_length=127)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    birthdate = models.DateField()
    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=63)
    province = models.CharField(max_length=63)
    country = models.CharField(max_length=63)
    phone_number = models.CharField(max_length=63)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnoses = models.CharField(max_length=255)
    notes = models.TextField()
    creator = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)

class Vitals(models.Model):
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    temperature = models.IntegerField()
    pulse = models.IntegerField()
    respiratory_rate = models.IntegerField()
    bp_systole = models.IntegerField()
    bp_diastole = models.IntegerField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    creator = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)

class LabResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=127)
    img = models.CharField(max_length=255)
    result = models.CharField(max_length=127)
    creator = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)

class Treatment(models.Model):
    DRUG_CHOICES = (
        ('HRZE', 'FDC 4 combination (HRZE)'),
        ('HR', 'FDC 2 combination (HR)'),
        ('H', 'Isoniazid (H)'),
        ('R', 'Rifampisin (R)'),
        ('Z', 'Pirazinamid (Z)'),
        ('E', 'Etambutol (E)'),
        ('S', 'Streptomisin (S)'),
        ('HRZ', 'FDC for children (HRZ)'),
        ('Km', 'Kanamysin (Km)'),
        ('Cm', 'Capreomysin (Cm)'),
        ('Lfx', 'Levofloksasin (Lfx)'),
        ('Mfx', 'Moksifloksasin (Mfx)'),
        ('Etio', 'Ethionamide (Etio)'),
        ('Cs', 'Cycloserine (Cs)'),
        ('PAS', 'Para-aminosalicyclic Acid (PAS)'),
    )
    medication = models.CharField(max_length=7, choices=DRUG_CHOICES)
    dosage = models.DecimalField(max_digits=15, decimal_places=2)
    freq_day = models.IntegerField()
    freq_week = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    creator = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)

class Appointment(models.Model):
    SERVICE_CHOICES = (
        ('C', 'Consultation'),
        ('L', 'Lab test'),
        ('M', 'Medical check up'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=255, choices=SERVICE_CHOICES)
    agenda = models.TextField()
    date = models.DateTimeField()
    creator = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)

class Screening(models.Model):
    HIV_CHOICES = (
        ('1', 'Yes'),
        ('0', 'No'),
        ('99', 'Unknown'),
    )
    TB_EXPOSURE_CHOICES = (
        ('1', 'One member of family in the same house had previous TB'),
        ('2', 'One member of family in the same house has active TB infection'),
        ('3', 'Contact with person infected with TB'),
        ('99', 'Unknown'),
    )
    DIAGNOSIS_CHOICES = (
        ('1', 'Suspect TB'),
        ('2', 'Confirm Positive TB'),
        ('0', 'Negative TB'),
    )
    TB_PATIENT_STATUS_CHOICES = (
        ('1', 'New'),
        ('2', 'Chronic'),
        ('3', 'Relapse'),
        ('4', 'Drop out'),
        ('99', 'NA'),
    )
    cough = models.BooleanField()
    haemoptysis = models.BooleanField()
    chest_pain = models.BooleanField()
    weight_loss = models.BooleanField()
    fatigue = models.BooleanField()
    fever = models.BooleanField()
    night_sweats = models.BooleanField()
    chills = models.BooleanField()
    other_symptoms = models.BooleanField()
    diagnosis = models.CharField(max_length=7, choices=DIAGNOSIS_CHOICES)
    tb_patient_status = models.CharField(max_length=7, choices=TB_PATIENT_STATUS_CHOICES, default=0)
    meningitis = models.BooleanField()
    pregnant = models.BooleanField()
    immunocompromised = models.BooleanField()
    malnutrition = models.BooleanField()
    coinfection = models.BooleanField()
    comorbid = models.BooleanField()
    hiv = models.CharField(max_length=15, choices=HIV_CHOICES)
    tb_exposure = models.CharField(max_length=7, choices=TB_EXPOSURE_CHOICES)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, default=1)
    date_created = models.DateTimeField(auto_now_add=True)