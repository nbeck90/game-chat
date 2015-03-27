from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
import factory


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'bob'
    password = factory.PostGenerationMethodCall('set_password', 'password')


class RegistrationLoginTests(TestCase):

    def setUp(self):
        self.bob = UserFactory.create()
        self.client = Client()

    def test_register_page_works(self):
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)

    def test_register_new_user(self):
        self.client.post('/accounts/register/',
                         {'username': 'toby',
                          'email': 'toby@example.com',
                          'password1': 'test',
                          'password2': 'test'}
                         )
        self.assertEqual(len(User.objects.all()), 2)


class HomePageTests(TestCase):

    def setUp(self):
        self.bob = UserFactory.create()
        self.client = Client()

    def test_empty_url_finds_home_page(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_sweet_game_pics_on_homepage(self):
        response = self.client.get('/')
        self.assertIn('smash.jpg', response.content)
        self.assertIn('wow.jpg', response.content)
        self.assertIn('lol.jpg', response.content)
        self.assertIn('csgo.jpg', response.content)
        self.assertIn('destiny.jpg', response.content)
        self.assertIn('mine.jpg', response.content)
        self.assertIn('hearth.jpg', response.content)
        self.assertIn('dota.jpg', response.content)
        self.assertIn('diablo.jpg', response.content)
        self.assertIn('dnd.jpg', response.content)


class TestRegistrationLogin(TestCase):

    def setUp(self):
        self.bob = UserFactory.create()
        self.bob_profile = self.bob.profile
        self.client = Client()

    def test_login_page_works(self):
        self.client.post(
            '/accounts/login/',
            {'username': "bob",
             'password': "password"}
            )
        self.assertIn('_auth_user_id', self.client.session)

    def test_register_page_works(self):
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)

    def test_register_new_user(self):
        self.client.post('/accounts/register/',
                         {'username': 'bobby',
                          'email': 'bobby@example.com',
                          'password1': 'test',
                          'password2': 'test'}
                         )
        self.assertEqual(len(User.objects.all()), 2)
