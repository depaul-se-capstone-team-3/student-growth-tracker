import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


USERNAME = 'Parent_One'
PASSWORD = 'test'


class ParentFunctionalTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
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

    def test_parent_can_log_in(self):
        self.browser.get(self.server_url)

        self.log_in()

        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Parent One Student Overview', header)

    def test_parent_can_view_class_details(self):
        self.browser.get(self.server_url)

        self.log_in()

        math_one_link = self.browser.find_element_by_id('class-1')
        math_one_link.click()

        header = self.browser.find_element_by_tag_name('h3').text
        self.assertIn('Math One', header)

    def test_parent_can_navigate(self):
        self.browser.get(self.server_url)
        self.log_in()
        
        #verify correct starting page view
        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Parent One Student Overview', header)
        
        #go to detail view for first class
        self.browser.find_element_by_id('class-0').click()
        
        #check to make sure Parent, Student, and Class are as expected
        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Parent One', header)
        header = self.browser.find_element_by_tag_name('h2')
        self.assertEqual('Student: Student One', header.text)
        header = self.browser.find_element_by_tag_name('h3')
        self.assertEqual('Language Arts One', header.text)
        grade_container = self.browser.find_element_by_id('student_grade_table')
        self.assertIsNotNone(grade_container)
        table_rows = grade_container.find_elements_by_tag_name('tr')
        
        #check that table has expected number of elements (headers are a row)
        self.assertEqual(len(table_rows), 12)
        
        #check a few elements of the table to see if they're correct
        row_list = table_rows[1].find_elements_by_tag_name('td')
        self.assertEqual(row_list[0].text, "LA Assignment One")
        self.assertEqual(row_list[1].text, "5.0 / 10.0")
        self.assertEqual(row_list[2].text, "Dec 08, 2015")
        row_list = table_rows[2].find_elements_by_tag_name('td')
        self.assertEqual(row_list[0].text, "LA Assignment Two")
        self.assertEqual(row_list[1].text, "10.0 / 10.0")
        self.assertEqual(row_list[2].text, "Dec 09, 2015")
        row_list = table_rows[6].find_elements_by_tag_name('td')
        self.assertEqual(row_list[0].text, "LA Assignment Six")
        self.assertEqual(row_list[1].text, "10.0 / 10.0")
        self.assertEqual(row_list[2].text, "Dec 15, 2015")
