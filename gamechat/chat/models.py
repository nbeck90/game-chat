from django.db import models
from profiles.models import Profile


class ChatRoom(models.Model):
    """
    Chat room model with a field to connect to the owner
    """
    name = models.CharField(max_length=200)
    main = models.CharField(max_length=200, default='halo')
    subscribers = models.ManyToManyField(Profile,
                                         related_name='subs')
    owner = models.OneToOneField(Profile, related_name='chat_room',
                                          blank=True, null=True)

    def __unicode__(self):
        return self.name

    def add_subscriber(self, profile):
        self.subscribers.add(profile)
