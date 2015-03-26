from django.db import models
from django.core.urlresolvers import reverse
from profiles.models import Profile


class Event(models.Model):
    creator = models.ForeignKey(Profile)
    title = models.CharField(max_length=200)
    date = models.DateField()
    attending = models.ManyToManyField(Profile,
    								  symmetrical=False,
                                      related_name='accepted_invites',
                                      blank=True,
                                      null=True)
    invitees = models.ManyToManyField(Profile,
    								  symmetrical=False,
                                      related_name='invited_to',
                                      blank=True,
                                      null=True)
