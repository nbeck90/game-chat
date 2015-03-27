from django.db import models
from profiles.models import Profile
from datetime import datetime


class Event(models.Model):

    creator = models.ForeignKey(Profile, related_name='created_events')
    title = models.CharField(max_length=200, null=False, blank=False)
    # date = models.DateField(default='2015-01-01')
    description = models.TextField(default="Type your info here")
    time = models.DateTimeField(default=datetime.now, blank=True)

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

    def __str__(self):
        return self.title
