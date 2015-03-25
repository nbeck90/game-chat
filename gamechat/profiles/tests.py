from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
import factory
from unittest import skip


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'bob'
    # password = factory.PostGenerationMethodCall('set_password', 'password')


# Create your tests here.
class ProfileCreationTests(TestCase):

    def setUp(self):
        self.bob = UserFactory.create()
        self.bob_profile = self.bob.profile

    def test_creating_user_creates_profile(self):
        assert self.bob.profile

    def test_new_profile_has_correct_defaults(self):
        assert self.bob_profile.user == self.bob
        assert self.bob_profile.picture == 'photos/link.jpg'
        assert self.bob_profile.friends.all().count() == 0
        assert self.bob_profile.blocking.all().count() == 0
        assert self.bob_profile.requested_friends.all().count() == 0
        assert self.bob_profile.slug == 'bob'
        assert self.bob_profile.Created_room is False
        assert self.bob_profile.chat_room_name is None


class ProfileMethodTests(TestCase):

    def setUp(self):
        self.bob = UserFactory.create()
        self.bob_profile = self.bob.profile
        self.alice = UserFactory.create(username='alice')
        self.alice_profile = self.alice.profile
        self.toby = UserFactory.create(username='toby')
        self.toby_profile = self.toby.profile

    def test_default_str(self):
        self.assertEqual(str(self.bob_profile), 'bob')

    def test_friending(self):
        self.assertEqual(self.bob_profile.friends.all().count(), 0)
        self.bob_profile.friending(self.alice_profile)
        self.assertIn(self.alice_profile, self.bob_profile.friends.all())

    def test_unfriending(self):
        self.bob_profile.friending(self.alice_profile)
        self.bob.profile.unfriending(self.alice_profile)
        self.assertNotIn(self.alice_profile, self.bob_profile.friends.all())

    def test_get_friends(self):
        self.bob_profile.friending(self.alice_profile)
        self.bob_profile.friending(self.toby_profile)
        self.assertIn(self.alice_profile, self.bob_profile.get_friends())
        self.assertIn(self.toby_profile, self.bob_profile.get_friends())

    def test_block(self):
        self.bob_profile.block(self.alice_profile)
        self.assertIn(self.alice_profile, self.bob_profile.blocking.all())

    def test_unblock(self):
        self.bob_profile.block(self.alice_profile)
        self.bob_profile.unblock(self.alice_profile)
        self.assertNotIn(self.alice_profile, self.bob_profile.blocking.all())

    def test_room_status(self):
        self.assertEqual(self.bob_profile.room_status(), False)

    def test_friending_blocked(self):
        self.bob_profile.block(self.alice_profile)
        with self.assertRaises(ValueError):
            self.alice_profile.friending(self.bob_profile)
