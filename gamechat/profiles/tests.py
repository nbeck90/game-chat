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
    password = factory.PostGenerationMethodCall('set_password', 'password')


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
        assert self.bob_profile.own_room is False
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


class ProfileViewsTests(TestCase):

    def setUp(self):
        self.bob = UserFactory.create()
        self.bob_profile = self.bob.profile
        self.alice = UserFactory.create(username='alice')
        self.alice_profile = self.alice.profile
        self.toby = UserFactory.create(username='toby')
        self.toby_profile = self.toby.profile
        self.client = Client()

    def test_you_cant_get_anywhere_unless_logged_in(self):
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/profile/bob/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/profile/profile_list')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/profile/request_friend/1')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/profile/add_friend/1')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/profile/block/1')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/profile/unblock/1')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/profile/picture/1')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/profile/accept_invite/1')
        self.assertEqual(response.status_code, 302)

    def test_profile_list(self):
        self.client.login(username='bob', password='password')
        response = self.client.get('/profile/profile_list')
        self.assertContains(response, '<a href="/profile/bob"><h1>bob</h1></a>')
        self.assertContains(response, '<a href="/profile/alice"><h1>alice</h1></a>')
        self.assertContains(response, '<a href="/profile/toby"><h1>toby</h1></a>')

    def test_view_profile(self):
        self.client.login(username='bob', password='password')
        response = self.client.get('/profile/')
        self.assertContains(response, '<h1>Welcome, bob!</h1>')

    def test_view_other_profile(self):
        self.client.login(username='bob', password='password')
        response = self.client.get('/profile/alice/')
        self.assertContains(response, '<h1>alice</h1>')

    def test_request_friend(self):
        self.client.login(username='bob', password='password')
        response = self.client.post('/profile/request_friend/40')
        self.assertIn(self.alice_profile, self.bob_profile.requested_friends.all())
        response = self.client.post('/profile/')
        self.assertContains(response, text)

    def test_add_friend(self):
        self.client.login(username='bob', password='password')
        response = self.client.post('/profile/request_friend/40')
        self.assertIn(self.alice_profile, self.bob_profile.requested_friends.all())

    def test_block_view(self):
        pass

    def test_unblock_view(self):
        pass

    def test_accept_invite(self):
        pass

    def test_update_picture(self):
        pass