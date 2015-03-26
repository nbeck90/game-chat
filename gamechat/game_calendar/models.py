from django.db import models
from django.core.urlresolvers import reverse
from profiles.models import Profile


class Event(models.Model):
    creator = models.ForeignKey(Profile)
    title = models.CharField(max_length=200)
    date = models.DateField()
