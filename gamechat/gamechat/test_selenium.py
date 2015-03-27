from __future__ import print_function

from django.test import LiveServerTestCase
from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from django.contrib.auth.models import User
# from imager_images.models import Photo, Album
import factory


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
        # self.driver2 = webdriver.Chrome()
        super(TestLogin, self).setUp()
        self.bob = UserFactory.create()
        self.bob_profile = self.bob.profile

    def tearDown(self):
        self.driver1.quit()
        # self.driver2.quit()
        super(TestLogin, self).tearDown()

    # def test_dueling_browsers(self):
    #     self.driver1.get(self.live_server_url)
    #     self.driver2.get(self.live_server_url)

    def test_chatroom_simple(self):
        # the user finds his way to homepage, and logs in
        self.driver1.get(self.live_server_url)
        self.assertIn('Login', self.driver1.page_source)
        self.driver1.find_element_by_link_text("Login").click()
        form = self.driver1.find_element_by_tag_name("form")
        username_field = self.driver1.find_element_by_id("id_username")
        username_field.send_keys("bob")
        password_field = self.driver1.find_element_by_id("id_password")
        password_field.send_keys("password")
        form.submit()

        # having logged in, the user sees his profile page.
        self.assertIn('Logout', self.driver1.page_source)
        self.assertIn('Welcome, bob!', self.driver1.page_source)

        # wanting to socialize with other nerds, the user goes back
        # to the homepage to look for chatrooms.
        self.driver1.self.driver1.find_element_by_link_text("Home").click()
        self.assertIn('Super Smash Brothers', self.driver1.page_source)
        self.assertIn('Destiny', self.driver1.page_source)

        # having seen a chatroom he/she'd like to visit, the user
        # enters the chat list, and looks for rooms.
        self.driver1.find_element_by_link_text("Destiny").click()
        self.assertIn('Available Chat Rooms for destiny', self.driver1.page_source)
        self.assertIn('No chats are available.', self.driver1.page_source)

        # seeing no chat rooms available, the user 

    # def test_unauthorized_index(self):
    #     self.driver.get(self.live_server_url)
    #     self.assertIn('Login', self.driver.page_source)
    #     self.assertIn('Register', self.driver.page_source)

    # def test_authorized_index(self):
    #     # try:
    #     self.driver.get(self.live_server_url)
    #     self.driver.find_element_by_link_text("Login").click()
    #     form = self.driver.find_element_by_tag_name("form")
    #     username_field = self.driver.find_element_by_id("id_username")
    #     username_field.send_keys("Bob")
    #     password_field = self.driver.find_element_by_id("id_password")
    #     password_field.send_keys("password")
    #     form.submit()
    #     self.assertIn('Bob', self.driver.page_source)
    #     self.assertIn('Library', self.driver.page_source)
    #     self.assertIn('Stream', self.driver.page_source)
    #     self.assertIn('Log out', self.driver.page_source)

    #     # except Exception as e:
    #     #     self.driver.save_screenshot('SCREEN_DUMP_LOCATION.png')
    #     #     raise e

    # def test_login_unauthorized_user(self):
    #     self.driver.get(self.live_server_url)
    #     self.driver.find_element_by_link_text("Login").click()
    #     form = self.driver.find_element_by_tag_name("form")
    #     username_field = self.driver.find_element_by_id("id_username")
    #     username_field.send_keys("Not a user")
    #     password_field = self.driver.find_element_by_id("id_password")
    #     password_field.send_keys("fake password")
    #     form.submit()
    #     self.assertIn('Please enter a correct username and password', self.driver.page_source)

    # def test_random_image(self):
    #     self.driver.get(self.live_server_url)
    #     self.assertIn('default_stock_photo', self.driver.page_source)
