from django.db import models
from gevent import queue
from profiles.models import Profile

# Create your models here.


class ChatRoom(models.Model):
    name = models.CharField(max_length=200)

    # queue = queue.Queue()
    subscribers = models.ManyToManyField(Profile,
                                         related_name='subs')
    owner = models.OneToOneField(Profile, related_name='chat_room',
                                    blank=True, null=True)

    def __unicode__(self):
        return self.name

    def backlog(self, size=25):
        pass
        # return self.messages[-size:]

    def add_subscriber(self, profile):
        self.subscribers.add(profile)
