from django.test import TestCase
from django.contrib.auth.models import User
from models import ChatRoom, Message
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
@skip('lkjf')
class CreateChatTests(TestCase):

    def setUp(self):
        self.bob = UserFactory.create()
        self.bob_profile = self.bob.profile
        self.bobs_chatroom = ChatRoomFactory.create(owner=self.bob_profile)
        self.alice = UserFactory.create(username='alice')
        self.alice_profile = self.alice.profile

    def test_chatroom_defaults(self):
        self.assertEqual(self.bobs_chatroom.name, 'bobschatroom')
        self.assertEqual(self.bobs_chatroom.owner, self.bob_profile)
        self.assertEqual(self.bobs_chatroom.subscribers.all().count(), 0)

    def test_add_subscriber(self):
        self.bobs_chatroom.add_subscriber(self.alice_profile)
        self.bobs_chatroom.add_subscriber(self.bob_profile)
        self.assertEqual(self.bobs_chatroom.subscribers.all().count(), 2)
        self.assertIn(self.alice_profile, self.bobs_chatroom.subscribers.all())
        self.assertIn(self.bob_profile, self.bobs_chatroom.subscribers.all())


class ChatRoomViewsTests(TestCase):

    def setUp(self):
        self.bob = UserFactory.create()
        self.bob_profile = self.bob.profile
        self.bobs_chatroom = ChatRoomFactory.create(owner=self.bob_profile)

    def test_Message(self):
        Message.objects.create(
            profile=self.bob_profile,
            room=self.bobs_chatroom,
            text=u"hello!")
        m1 = Message.objects.get(profile=self.bob_profile)
        print m1
