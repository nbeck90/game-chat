from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from models import ChatRoom
import factory
from unittest import skip


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'bob'
    # password = factory.PostGenerationMethodCall('set_password', 'password')


class ChatRoomFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ChatRoom
        django_get_or_create = ('owner',)

    owner = UserFactory.create()
    name = 'bobschatroom'


# Create your tests here.
class CreateChatTests(TestCase):

    def setUp(self):
        self.bob = UserFactory.create()
        self.bob_profile = self.bob.profile
        self.bobs_chatroom = ChatRoomFactory.create(owner=self.bob_profile)

    def test_chatroom_defaults():
        pass


class ChatRoomTests(TestCase):

    def setUp(self):
        self.bob = UserFactory.create()
        self.bob_profile = self.bob.profile
        self.bobs_chatroom = ChatRoomFactory.create(owner=self.bob_profile)
