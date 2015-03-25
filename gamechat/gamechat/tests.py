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


class LoginTests(TestCase):

    def setUp(self):
        self.bob = UserFactory.create()
        self.client = Client()

    # def setUp(self):
    #     self.bob = UserFactory.create()
    #     self.alice = UserFactory.create(username='Alice')
    #     self.bobphoto = PhotoFactory.create(profile=self.bob.ImagerProfile)
    #     self.publicbobphoto = PhotoFactory.create(profile=self.bob.ImagerProfile,
    #                                               published='pb')

    def test_empty_url_finds_home_page(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_sweet_game_pics_on_homepage(self):
        response = self.client.get('/')
        self.assertIn('smash.jpg', response)

    def test_home_page_photo_is_stock_if_no_user_photos(self):
        self.publicbobphoto.delete()
        response = self.client.get('/')
        self.assertEqual(
            response.context['random_photo'],
            self.STOCKPHOTO_URL)


class TestRegistrationViews(TestCase):

    def setUp(self):
        self.client = Client()

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
        self.assertEqual(len(User.objects.all()), 1)



