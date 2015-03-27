from django.db import models
from profiles.models import Profile


class Event(models.Model):
    creator = models.ForeignKey(Profile, related_name='created_events')
    title = models.CharField(max_length=200)
    date = models.DateField(default='2015-01-01')
    attending = models.ManyToManyField(
        Profile,
        symmetrical=False,
        related_name='accepted_invites',
        blank=True,
        null=True)
    invitees = models.ManyToManyField(
        Profile,
        symmetrical=False,
        related_name='invited_to',
        blank=True,
        null=True)
