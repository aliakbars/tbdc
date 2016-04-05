from django.core.management.base import BaseCommand, CommandError
from patient.models import *

class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('patient_id', nargs='+', type=str)

    def handle(self, *args, **options):
        for pid in options['patient_id']:
            try:
                patient = Patient.objects.get(identifier=pid)
            except Patient.DoesNotExist:
                raise CommandError('Patient %s does not exist' % pid)

            self.stdout.write('SMS sent to patient %s!' % pid)