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
    owner = models.OneToOneField(Profile,
                                 related_name='chat_room',
                                 blank=True, null=True)

    from collections import deque

    active_messages = deque()

    def __unicode__(self):
        return self.name

    def add_subscriber(self, profile):
        self.subscribers.add(profile)

    def add_message(self, message):
        while len(self.active_messages) >= 30:
            self.active_messages.pop()

        self.active_messages.appendleft(message)

    def trunctate_message_set(self):
        while self.message_set.all().count() >= 40:
            self.message_set.order_by('date')[0].delete()


class Message(models.Model):
    """
    Model for messages submitted by users and held by chat room
    """
    from datetime import datetime

    text = models.TextField(default="")

    date = models.DateTimeField(default=datetime.now, blank=True)

    profile = models.ForeignKey(Profile, related_name='messages')

    room = models.ForeignKey(ChatRoom)

    def __str__(self):
        return self.text
