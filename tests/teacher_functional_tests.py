import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select


USERNAME = 'tedwhitrock'
PASSWORD = 'test'


class TeacherFunctionalTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.server_url = 'http://localhost:8000/student_growth_tracker/'
        self.browser.implicitly_wait(10)

    def tearDown(self):
        self.browser.quit()

    def log_in(self):
        uname_input = self.browser.find_element_by_id('auth_user_username')
        uname_input.send_keys(USERNAME)
        pwd_input = self.browser.find_element_by_id('auth_user_password')
        pwd_input.send_keys(PASSWORD)
        pwd_input.send_keys(Keys.ENTER)

    def test_correct_page_loads(self):
        """
        Test that:

        #. the login page displays by default.
        """
        self.browser.get(self.server_url)

        # Get the "logo" text to make sure we're on the correct page.
        self.assertIn('Student Growth Tracker', self.browser.title)
        logo_text = self.browser.find_element_by_id('web2py-logo').text
        self.assertIn('Student Growth Tracker', logo_text)

    def test_teacher_can_log_in(self):
        """
        Test that:

        #. the teacher can log in,
        #. the gradebook is displayed upon login.
        """
        self.browser.get(self.server_url)

        self.log_in() # Gradebook

        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn("Ted Whitrock's Gradebook", header)

    def test_teacher_can_view_class(self):
        """
        Test that:

        #. the teacher can access the overview for a specific class.
        """
        self.browser.get(self.server_url)

        self.log_in() # Gradebook
        self.browser.find_element_by_link_text('Math One').click() # Math One class overview

        # The first 'h1' tag should have a link with text == class name.
        header = self.browser.find_element_by_xpath('//h1/a').text
        self.assertIn('Math One', header)

    def test_teacher_can_view_class_details(self):
        """
        Test that:

        #. the teacher can access the grade details for a specific class.
        """
        self.browser.get(self.server_url)

        self.log_in() # Gradebook
        self.browser.find_element_by_link_text('Math One').click() # Math One class overview
        self.browser.find_element_by_link_text('Math One').click() # Math One class details

        # The first 'h1' text should contain the class name.
        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Math One', header)

    def test_teacher_grade_table_displays(self):
        """
        Test that:

        #. the teacher can view the grade detail table for a specific class.
        """
        self.browser.get(self.server_url)

        self.log_in() # Gradebook
        self.browser.find_element_by_link_text('Math One').click() # Math One class overview
        self.browser.find_element_by_link_text('Math One').click() # Math One class details

        # Find the div that should contain the table of grades.
        grade_container = self.browser.find_element_by_id('student_grades')
        self.assertIsNotNone(grade_container)

        # Find the table that contains the grades.
        grade_table = grade_container.find_element_by_tag_name('table')
        self.assertIsNotNone(grade_table)

        header_row = grade_table.find_element_by_tag_name('tr')
        header_columns = header_row.find_elements_by_tag_name('td')
        self.assertEqual('Math Assignment Eleven', header_columns[1].text)

    def test_teacher_add_new_assignment(self):
        """
        Test that:

        #. the teacher can create a new assignment for the class.
        #. the assignment shows up in the grade table.
        """
        self.browser.get(self.server_url)

        self.log_in() # Gradebook
        self.browser.find_element_by_link_text('Math One').click() # Math One class overview
        self.browser.find_element_by_link_text('Math One').click() # Math One class details
        grade_container = self.browser.find_element_by_id('student_grades')
        grade_table = grade_container.find_element_by_tag_name('table')
        header_row = grade_table.find_element_by_tag_name('tr')
        header_columns = header_row.find_elements_by_tag_name('td')
        num_assignments = len(header_columns)

        # Navigate directly to the new assignment page.
        self.browser.get(self.server_url + 'grades/create/2/2')

        # Add a name
        assignment_name_input = self.browser.find_element_by_id('no_table_name')
        assignment_name_input.send_keys('new test assignment')

        # Add a grade type
        grade_type_selector = Select(self.browser.find_element_by_id('no_table_grade_type'))
        grade_type_selector.select_by_visible_text('Assignment')

        # Add a score
        score_input = self.browser.find_element_by_id('no_table_score')
        score_input.send_keys('20')

        # Add a standard
        standard_selector = Select(self.browser.find_element_by_id('no_table_standard'))
        standard_selector.select_by_value('10')

        # Submit the new grade.
        submit_button = self.browser.find_element_by_xpath("//input[@type='submit']")
        submit_button.click()

        # Make sure we've redirected back to the grade deatils page.
        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Math One', header)

        # Find the div that should contain the table of grades.
        grade_container = self.browser.find_element_by_id('student_grades')
        self.assertIsNotNone(grade_container)

        # Find the table that contains the grades.
        grade_table = grade_container.find_element_by_tag_name('table')
        self.assertIsNotNone(grade_table)

        header_row = grade_table.find_element_by_tag_name('tr')
        header_columns = header_row.find_elements_by_tag_name('td')
        new_assignment_column = header_columns[len(header_columns) - 1]
        self.assertEqual('new test assignment', new_assignment_column.text)
        self.assertEqual(num_assignments + 1, len(header_columns))
        self.assertEqual('new test assignment', new_assignment_column.text)

    def test_add_new_assignment_requires_name(self):
        pass

    def test_add_new_assignment_requires_grade_type(self):
        pass

    def test_add_new_assignment_requires_score(self):
        pass

    def test_add_new_assignment_requires_standard(self):
        pass
