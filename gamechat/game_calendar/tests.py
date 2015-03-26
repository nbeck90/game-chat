from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from models import Event
import factory
from unittest import skip


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'bob'
    password = factory.PostGenerationMethodCall('set_password', 'password')


class EventFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Event
        django_get_or_create = ('creator',)

    creator = UserFactory.create().profile


class EventCreationTests(TestCase):

    def setUp(self):
        self.bob = UserFactory.create()
        self.bob_profile = self.bob.profile
        self.bob_event = EventFactory.create(creator=self.bob_profile)

    def test_new_event_has_correct_defaults(self):
        self.assertEqual(self.bob_event.creator, self.bob_profile)
        self.assertEqual(self.bob_event.title, '')
        self.assertEqual(self.bob_event.date, '2015-01-01')


class CalendarViewTests(TestCase):

    def setUp(self):
        self.bob = UserFactory.create()
        self.bob_profile = self.bob.profile
        self.alice = UserFactory.create(username='alice')
        self.alice_profile = self.alice.profile
        self.bob_event = EventFactory.create(creator=self.bob_profile,
                                              title='bob_event',
                                              date='2015-03-01')
        self.bob_event2 = EventFactory.create(creator=self.bob_profile,
                                              title='bob_event2',
                                              date='2015-03-02')
        self.alice_event = EventFactory.create(creator=self.alice_profile,
                                              title='alice_event',
                                              date='2015-03-02')
        self.client = Client()

    @skip('broken test')
    def test_events_are_returned_with_return_event(self):
        self.client.login(username='bob', password='password')
        response = self.client.get('/calendar/event_feed/')

    def test_calendar_view_dispays_calendar_object(self):
        self.client.login(username='bob', password='password')
        response = self.client.get('/calendar/')
        self.assertContains(response, "<div id='calendar'></div>")

    def test_create_event_works(self):
        self.client.login(username='bob', password='password')
        self.assertEqual(Event.objects.all().count(), 2)
        self.client.post(
            '/calendar/create_event/',
            {'title': "bob's new event",
             'date': "2015-03-02"}
            )
        self.assertEqual(Event.objects.all().count(), 3)
