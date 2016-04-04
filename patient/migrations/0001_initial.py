# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('service_type', models.CharField(max_length=255)),
                ('agenda', models.TextField()),
                ('date', models.DateTimeField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LabResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('test_name', models.CharField(max_length=127)),
                ('img', models.CharField(max_length=255)),
                ('result', models.CharField(max_length=127)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=127)),
                ('last_name', models.CharField(max_length=127)),
                ('gender', models.CharField(default='M', max_length=1, choices=[('M', 'Male'), ('F', 'Female')])),
                ('birthdate', models.DateField()),
                ('address', models.CharField(max_length=255)),
                ('address2', models.CharField(max_length=255, null=True)),
                ('city', models.CharField(max_length=63)),
                ('province', models.CharField(max_length=63)),
                ('country', models.CharField(max_length=63)),
                ('phone_number', models.CharField(max_length=63)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.PROTECT)),
            ],
        ),
        migrations.CreateModel(
            name='Screening',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cough', models.BooleanField()),
                ('haemoptysis', models.BooleanField()),
                ('chest_pain', models.BooleanField()),
                ('weight_loss', models.BooleanField()),
                ('fatigue', models.BooleanField()),
                ('fever', models.BooleanField()),
                ('night_sweats', models.BooleanField()),
                ('chills', models.BooleanField()),
                ('other_symptoms', models.BooleanField()),
                ('diagnosis', models.CharField(max_length=7, choices=[('1', 'Suspect TB'), ('2', 'Confirm Positive TB'), ('0', 'Negative TB')])),
                ('tb_patient_status', models.CharField(default=0, max_length=7, choices=[('1', 'New'), ('2', 'Chronic'), ('3', 'Relapse'), ('4', 'Drop out'), ('0', 'NA')])),
                ('meningitis', models.BooleanField()),
                ('pregnant', models.BooleanField()),
                ('immunocompromised', models.BooleanField()),
                ('malnutrition', models.BooleanField()),
                ('coinfection', models.BooleanField()),
                ('comorbid', models.BooleanField()),
                ('hiv', models.CharField(max_length=15, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unknown', 'Unknown')])),
                ('tb_exposure', models.CharField(max_length=7, choices=[('1', 'One member of family in the same house had previous TB'), ('2', 'One member of family in the same house has active TB infection'), ('3', 'Contact with person infected with TB'), ('99', 'Unknown')])),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(to='patient.Patient')),
            ],
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('medication', models.CharField(max_length=7, choices=[('HRZE', 'FDC 4 combination (HRZE)'), ('HR', 'FDC 2 combination (HR)'), ('H', 'Isoniazid (H)'), ('R', 'Rifampisin (R)'), ('Z', 'Pirazinamid (Z)'), ('E', 'Etambutol (E)'), ('S', 'Streptomisin (S)'), ('HRZ', 'FDC for children (HRZ)'), ('Km', 'Kanamysin (Km)'), ('Cm', 'Capreomysin (Cm)'), ('Lfx', 'Levofloksasin (Lfx)'), ('Mfx', 'Moksifloksasin (Mfx)'), ('Etio', 'Ethionamide (Etio)'), ('Cs', 'Cycloserine (Cs)'), ('PAS', 'Para-aminosalicyclic Acid (PAS)')])),
                ('dosage', models.DecimalField(max_digits=15, decimal_places=2)),
                ('freq_day', models.IntegerField()),
                ('freq_week', models.IntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(to='patient.Patient')),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('diagnoses', models.CharField(max_length=255)),
                ('notes', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(to='patient.Patient')),
            ],
        ),
        migrations.CreateModel(
            name='Vitals',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('height', models.DecimalField(max_digits=5, decimal_places=2)),
                ('weight', models.DecimalField(max_digits=5, decimal_places=2)),
                ('temperature', models.IntegerField()),
                ('pulse', models.IntegerField()),
                ('respiratory_rate', models.IntegerField()),
                ('bp_systole', models.IntegerField()),
                ('bp_diastole', models.IntegerField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(to='patient.Patient')),
            ],
        ),
        migrations.AddField(
            model_name='labresult',
            name='patient',
            field=models.ForeignKey(to='patient.Patient'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(to='patient.Patient'),
        ),
    ]
