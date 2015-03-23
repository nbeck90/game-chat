from django.db import models

# Create your models here.


class ChatRoom(models.Model):
    name = models.CharField(max_length=200)

    messages = []

    def __unicode__(self):
        return self.name

    def backlog(self, size=25):
        return self.messages[-size:]

    def add(self, message):
        self.messages.append(message)