import re
import threading
import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from app import create_app, db, fake
from app.models import Role, User


class SeleniumTestCase(unittest.TestCase):
    client = None
    wait = None

    @classmethod
    def setUpClass(cls):
        # start Chrome
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')

        try:
            cls.client = webdriver.Chrome(chrome_options=options)
            cls.wait = WebDriverWait(cls.client, 10)
        except:
            pass

        # skip these tests if the browser could not be started
        if cls.client:
            # create the application
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            # suppress logging to keep unittest output clean
            # import logging
            # logger = logging.getLogger('werkzeug')
            # logger.setLevel("ERROR")

            # create the database and populate with some fake data
            db.create_all()
            Role.insert_roles()
            fake.users(10)
            fake.posts(10)

            # add an administrator user
            admin_role = Role.query.filter_by(permissions=0xff).first()
            admin = User(email='david@example.com',
                         username='david', password='123456',
                         role=admin_role, confirmed=True)
            db.session.add(admin)
            db.session.commit()

            # start the Flask server in a thread
            cls.server_thread = threading.Thread(target=cls.app.run, kwargs={'debug': False})
            cls.server_thread.start()

            # give the server a second to ensure it is up
            time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            # stop the Flask server and the browser
            cls.client.get('http://localhost:5000/shutdown')
            cls.client.quit()
            cls.server_thread.join()

            # destroy database
            db.drop_all()
            db.session.remove()

            # remove application context
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self):
        pass

    def test_admin_home_page(self):
        # navigate to home page
        self.client.get('http://localhost:5000/')
        self.assertTrue(re.search('Hello,\s+Stranger!', self.client.page_source))

        # navigate to login page
        self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[text()="Log In"]')))
        self.client.find_element_by_link_text('Log In').click()
        self.assertIn('<h1>Login Form</h1>', self.client.page_source)

        admin = User.query.filter_by(email='david@example.com').first()
        self.assertEqual(admin.username, 'david')

        # login
        time.sleep(1)
        self.client.find_element_by_name('email').send_keys('david@example.com')
        self.client.find_element_by_name('password').send_keys('123456')
        self.client.find_element_by_name('submit').click()
        time.sleep(1)
        self.assertTrue(re.search('Hello,\s+david!', self.client.page_source))

        # navigate to the user's profile page
        self.client.find_element_by_link_text('Profile').click()
        time.sleep(1)
        self.assertIn('<span>david</span>', self.client.page_source)

