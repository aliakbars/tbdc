from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Chat(models.Model):
    content = models.TextField()
    sender = models.ForeignKey(User)
    receiver = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)