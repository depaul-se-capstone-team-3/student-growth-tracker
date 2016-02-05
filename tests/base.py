import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select


class FunctionalTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.server_url = 'http://localhost:8000/student_growth_tracker/'
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()

    def log_in(self):
        uname_input = self.browser.find_element_by_id('auth_user_username')
        uname_input.send_keys(self.username)
        pwd_input = self.browser.find_element_by_id('auth_user_password')
        pwd_input.send_keys(self.password)
        pwd_input.send_keys(Keys.ENTER)
