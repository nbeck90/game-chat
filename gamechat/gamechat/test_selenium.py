from __future__ import print_function

from django.test import LiveServerTestCase
from selenium import webdriver
import os
from django.contrib.auth.models import User
# from imager_images.models import Photo, Album
import factory
import time

SCREEN_DUMP_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'screendumps'
)


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'bob'
    password = factory.PostGenerationMethodCall('set_password', 'password')


class TestLogin(LiveServerTestCase):

    def setUp(self):
        self.driver1 = webdriver.Firefox()
        self.driver2 = webdriver.Chrome()
        super(TestLogin, self).setUp()
        self.bob = UserFactory.create()
        self.bob_profile = self.bob.profile
        self.alice = UserFactory.create(username='alice')
        self.alice_profile = self.alice.profile

    def tearDown(self):
        self.driver1.quit()
        self.driver2.quit()
        super(TestLogin, self).tearDown()

    def test_chatroom_simple(self):
        # bob finds his way to homepage, and logs in
        self.driver1.get(self.live_server_url)
        self.assertIn('Login', self.driver1.page_source)
        self.driver1.find_element_by_link_text("Login").click()
        form = self.driver1.find_element_by_tag_name("form")
        username_field = self.driver1.find_element_by_id("id_username")
        username_field.send_keys("bob")
        password_field = self.driver1.find_element_by_id("id_password")
        password_field.send_keys("password")
        form.submit()

        # having logged in, bob sees his profile page.
        self.assertIn('Logout', self.driver1.page_source)
        self.assertIn('Welcome, bob!', self.driver1.page_source)

        # wanting to socialize with other nerds, bob goes back
        # to the homepage to look for chatrooms.
        self.driver1.find_element_by_link_text("Home").click()
        self.assertIn('Super Smash Brothers', self.driver1.page_source)
        self.assertIn('Destiny', self.driver1.page_source)

        # having seen a chatroom bob'd like to visit, bob
        # enters the chat list, and looks for rooms.
        self.driver1.find_element_by_link_text("Destiny").click()
        self.assertIn('Available Chat Rooms', self.driver1.page_source)
        self.assertIn('No chats are available.', self.driver1.page_source)

        # seeing no chat rooms available, bob decides to creates one.
        form = self.driver1.find_element_by_tag_name("form")
        chat_name = self.driver1.find_element_by_name("Enter a New Room Name")
        chat_name.send_keys("I like Destiny's Child")
        form.submit()

        # inside the chatroom, bob sees that he is the only
        # subscriber. Bob sadly writes messages to himself.
        form = self.driver1.find_element_by_tag_name("form")
        message_field = self.driver1.find_element_by_id("messageinput")
        message_field.send_keys("I like Destinys Child!")
        form.submit()
        time.sleep(1)
        self.assertIn('<li>bob: I like Destinys Child!</li>',
                      self.driver1.page_source)

        # sad, lonely, and unfulfilled, bob logs out.
        self.driver1.find_element_by_link_text("Logout").click()
        self.assertIn('Login', self.driver1.page_source)

    def test_dueling_drivers(self):
        # bob finds his way to homepage, and logs in
        self.driver1.get(self.live_server_url)
        self.assertIn('Login', self.driver1.page_source)
        self.driver1.find_element_by_link_text("Login").click()
        form = self.driver1.find_element_by_tag_name("form")
        username_field = self.driver1.find_element_by_id("id_username")
        username_field.send_keys("bob")
        password_field = self.driver1.find_element_by_id("id_password")
        password_field.send_keys("password")
        form.submit()

        # having logged in, the bob sees his profile page.
        self.assertIn('Logout', self.driver1.page_source)
        self.assertIn('Welcome, bob!', self.driver1.page_source)

        # wanting to socialize with other nerds, bob goes back
        # to the homepage to look for chatrooms.
        self.driver1.find_element_by_link_text("Home").click()
        self.assertIn('Super Smash Brothers', self.driver1.page_source)
        self.assertIn('Destiny', self.driver1.page_source)

        # having seen a chatroom bob'd like to visit, he
        # enters the chat list, and looks for rooms.
        self.driver1.find_element_by_link_text("Destiny").click()
        self.assertIn('Available Chat Rooms', self.driver1.page_source)
        self.assertIn('No chats are available.', self.driver1.page_source)

        # seeing no chat rooms available, bob decides to creates one.
        form = self.driver1.find_element_by_tag_name("form")
        chat_name = self.driver1.find_element_by_name("Enter a New Room Name")
        chat_name.send_keys("destinychat")
        form.submit()

        # alice goes to elleffgee.com, looking for someone to chat with.
        self.driver2.get(self.live_server_url)
        self.assertIn('Login', self.driver2.page_source)
        self.driver2.find_element_by_link_text("Login").click()
        form = self.driver2.find_element_by_tag_name("form")
        username_field = self.driver2.find_element_by_id("id_username")
        username_field.send_keys("alice")
        password_field = self.driver2.find_element_by_id("id_password")
        password_field.send_keys("password")
        form.submit()

        # having logged in, alice sees her profile page.
        self.assertIn('Logout', self.driver2.page_source)
        self.assertIn('Welcome, alice!', self.driver2.page_source)

        # wanting to socialize with other nerds, alice goes back
        # to the homepage to look for chatrooms.
        self.driver2.find_element_by_link_text("Home").click()
        self.assertIn('Super Smash Brothers', self.driver2.page_source)
        self.assertIn('Destiny', self.driver2.page_source)

        # having seen a chatroom alice would like to visit, she
        # enters the chat list, and looks for rooms.
        self.driver2.find_element_by_link_text("Destiny").click()
        self.assertIn('destinychat', self.driver2.page_source)
        self.driver2.find_element_by_partial_link_text("destinychat").click()
        time.sleep(2)

        # seeing someone, else, alice sends a message:
        form = self.driver2.find_element_by_tag_name("form")
        message_field = self.driver2.find_element_by_id("messageinput")
        message_field.send_keys("Hello?")
        form.submit()

        # bob sees message, and responds:
        time.sleep(2)
        self.assertIn('<li>alice: Hello?</li>', self.driver1.page_source)
        form = self.driver1.find_element_by_tag_name("form")
        message_field = self.driver1.find_element_by_id("messageinput")
        message_field.send_keys("Hello!")
        form.submit()

        # alice sees bob's message, and responds:
        time.sleep(2)
        self.assertIn('<li>bob: Hello!</li>', self.driver2.page_source)
        form = self.driver2.find_element_by_tag_name("form")
        message_field = self.driver2.find_element_by_id("messageinput")
        message_field.send_keys("asl")
        form.submit()

        # bob, offended, leaves to block alice:
        time.sleep(2)
        self.assertIn('<li>alice: asl</li>', self.driver1.page_source)
        self.driver1.find_element_by_link_text("Profile List").click()
        self.driver1.find_element_by_link_text("alice").click()
        self.driver1.find_element_by_link_text("Block User").click()

        # alice tries again:
        form = self.driver2.find_element_by_tag_name("form")
        message_field = self.driver2.find_element_by_id("messageinput")
        message_field.send_keys("seriously asl")
        form.submit()

        # bob goes back to the home page and finds that all or alices
        # messages are blocked
        self.driver1.find_element_by_link_text("Home").click()
        self.driver1.find_element_by_link_text("Destiny").click()
        self.driver1.find_element_by_partial_link_text("destinychat").click()
        time.sleep(2)

        # alice tries one more time:
        form = self.driver2.find_element_by_tag_name("form")
        message_field = self.driver2.find_element_by_id("messageinput")
        message_field.send_keys("asl stands for age sex location")
        form.submit()

        # bob sees that alices messages are now blocked
        time.sleep(2)
        self.assertIn('<li>alice: blocked</li>', self.driver1.page_source)
        time.sleep(5)
