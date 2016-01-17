import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


PROFILE_DIRECTORY = r'/Users/bryan/Library/Application Support/Firefox/Profiles/mtgfc09j.selenium-testing'
USERNAME = 'Student_One'
PASSWORD = 'test'


class StudentFunctionalTest(unittest.TestCase):

    def setUp(self):
        profile = webdriver.firefox.firefox_profile.FirefoxProfile(profile_directory=PROFILE_DIRECTORY)
        self.browser = webdriver.Firefox(firefox_profile=profile)
        self.server_url = 'http://localhost:8000/student_growth_tracker/'
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()

    def log_in(self):
        uname_input = self.browser.find_element_by_id('auth_user_username')
        uname_input.send_keys(USERNAME)
        pwd_input = self.browser.find_element_by_id('auth_user_password')
        pwd_input.send_keys(PASSWORD)
        pwd_input.send_keys(Keys.ENTER)

    def test_correct_page_loads(self):
        self.browser.get(self.server_url)

        # Get the "logo" text to make sure we're on the correct page.
        self.assertIn('Student Growth Tracker', self.browser.title)
        logo_text = self.browser.find_element_by_id('web2py-logo').text
        self.assertIn('Student Growth Tracker', logo_text)

    def test_student_can_log_in(self):
        self.browser.get(self.server_url)

        self.log_in()

        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Student One', header)

    def test_student_can_view_class_details(self):
        self.browser.get(self.server_url)

        self.log_in()

        math_one_link = self.browser.find_element_by_link_text('Math One')
        math_one_link.click()

        header = self.browser.find_element_by_tag_name('h3').text
        self.assertIn('Math One', header)

        # row_text = 'Math Assignment Eleven'
        # table = self.browser.find_element_by_tag_name('table')
        # rows = table.find_elements_by_tag_name('tr')
        # self.assertIn(row_text, [row.text for row in rows])
