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

    def __unicode__(self):
        return self.name

    def add_subscriber(self, profile):
        self.subscribers.add(profile)

    def remove_subscriber(self, profile):
        self.subscribers.remove(profile)
        print "!!!!!!!!!!!!"
        print self.subscribers.all()

    def trunctate_message_set(self):
        while self.message_set.all().count() >= 20:
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
