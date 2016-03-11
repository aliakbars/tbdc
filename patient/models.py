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
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=255)
    agenda = models.TextField()
    date = models.DateTimeField()
    creator = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)