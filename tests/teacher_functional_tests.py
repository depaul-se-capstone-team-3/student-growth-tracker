from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select

from .base import FunctionalTest, TEACHER_USER_NAME, TEACHER_PASSWORD


class TeacherFunctionalTest(FunctionalTest):

    username = TEACHER_USER_NAME
    password = TEACHER_PASSWORD

    def test_correct_page_loads(self):
        """
        Test that:

        1. The login page displays by default.
        """
        self.browser.get(self.server_url)

        # Get the "logo" text to make sure we're on the correct page.
        self.assertIn('Student Growth Tracker', self.browser.title)
        logo_text = self.browser.find_element_by_id('web2py-logo').text
        self.assertIn('Student Growth Tracker', logo_text)

    def test_teacher_can_log_in(self):
        """
        Test that:

        1. The teacher can log in,
        2. The gradebook is displayed upon login.
        """
        self.browser.get(self.server_url)

        self.log_in() # Gradebook

        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn("Ted Whitrock's Gradebook", header)

    def test_teacher_can_view_class(self):
        """
        Test that:

        1. The teacher can access the overview for a specific class.
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

        1. The teacher can access the grade details for a specific class.
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

        1. The teacher can view the grade detail table for a specific class.
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
        header_columns = header_row.find_elements_by_tag_name('th')
        self.assertTrue(header_columns[1].text.startswith('Math Assignment'))

    def test_teacher_add_new_assignment(self):
        """
        Test that:

        1. The teacher can create a new assignment for the class.
        2. The assignment shows up in the grade table.
        """
        self.browser.get(self.server_url)

        self.log_in() # Gradebook
        self.browser.find_element_by_link_text('Math One').click() # Math One class overview
        self.browser.find_element_by_link_text('Math One').click() # Math One class details

        grade_container = self.browser.find_element_by_id('student_grades')
        grade_table = grade_container.find_element_by_tag_name('table')
        header_row = grade_table.find_element_by_tag_name('tr')
        header_columns = header_row.find_elements_by_tag_name('th')
        num_assignments = len(header_columns)

        # Check that the "Create new assignment" button takes us to
        # the create assignment page.
        new_assignment_button = self.browser.find_element_by_xpath("//div[@class='col-sm-4']/button")
        new_assignment_button.click()

        # Make sure we've landed on the create grade page.
        add_grade_header = self.browser.find_element_by_tag_name('h1')
        self.assertEqual('Create a Grade', add_grade_header.text)

        # Add a name
        assignment_name_input = self.browser.find_element_by_id('grade_name')
        assignment_name_input.send_keys('new test assignment')

        display_date_input = self.browser.find_element_by_id('grade_display_date')
        display_date_input.clear()
        display_date_input.send_keys('December 31, 2025')

        date_assigned_input = self.browser.find_element_by_id('grade_date_assigned')
        date_assigned_input.clear()
        date_assigned_input.send_keys('December 31, 2025')

        # Add a sufficiently distant due date so the
        # grade shows up as the last thing in the table.
        due_date_input = self.browser.find_element_by_id('grade_due_date')
        due_date_input.clear()
        due_date_input.send_keys('December 31, 2025')

        # Add a grade type
        grade_type_selector = Select(self.browser.find_element_by_id('grade_grade_type'))
        grade_type_selector.select_by_visible_text('Assignment')

        # Add a score
        score_input = self.browser.find_element_by_id('grade_score')
        score_input.send_keys('20')

        # Add a standard
        standard_selector = Select(self.browser.find_element_by_id('standards'))
        standard_selector.select_by_value('10')

        # Submit the new grade.
        submit_button = self.browser.find_element_by_xpath("//input[@type='submit']")
        submit_button.click()

        # Make sure we've redirected back to the grade deatils page.
        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Math One', header)

        # Find the div that should contain the table of grades.
        updated_grade_container = self.browser.find_element_by_id('student_grades')
        self.assertIsNotNone(grade_container)

        # Find the table that contains the grades.
        updated_grade_table = updated_grade_container.find_element_by_tag_name('table')
        self.assertIsNotNone(grade_table)

        updated_header_row = updated_grade_table.find_element_by_tag_name('tr')
        updated_header_columns = updated_header_row.find_elements_by_tag_name('th')

        last_column_index = len(updated_header_columns) - 1
        new_assignment_column = updated_header_columns[last_column_index]

        self.assertTrue(new_assignment_column.text.startswith('new test assignment'))
        self.assertEqual(num_assignments + 1, len(updated_header_columns))

    def test_teacher_add_new_assignment_requires_name(self):
        self.browser.get(self.server_url)

        self.log_in() # Gradebook
        self.browser.find_element_by_link_text('Math One')

        # Navigate directly to the new assignment page.
        self.browser.get(self.server_url + 'grades/create/2/2')

        # Make sure we're on the create grade page.
        add_grade_header = self.browser.find_element_by_tag_name('h1')
        self.assertEqual('Create a Grade', add_grade_header.text)

        # Add a grade type
        grade_type_selector = Select(self.browser.find_element_by_id('grade_grade_type'))
        grade_type_selector.select_by_visible_text('Assignment')

        # Add a score
        score_input = self.browser.find_element_by_id('grade_score')
        score_input.send_keys('20')

        # Add a standard
        standard_selector = Select(self.browser.find_element_by_id('standards'))
        standard_selector.select_by_value('10')

        # Submit without adding a grade type.
        submit_button = self.browser.find_element_by_xpath("//input[@type='submit']")
        submit_button.click()

        # Make sure we're still on the create grade page.
        add_grade_header = self.browser.find_element_by_tag_name('h1')
        self.assertEqual('Create a Grade', add_grade_header.text)

        # Find the error for the grade type.
        name_error = self.browser.find_element_by_id('name__error')
        self.assertIsNotNone(name_error)
        self.assertEqual('Enter a value', name_error.text)

    def test_teacher_add_new_assignment_requires_grade_type(self):
        self.browser.get(self.server_url)

        self.log_in() # Gradebook
        self.browser.find_element_by_link_text('Math One')

        # Navigate directly to the new assignment page.
        self.browser.get(self.server_url + 'grades/create/2/2')

        # Make sure we're on the create grade page.
        add_grade_header = self.browser.find_element_by_tag_name('h1')
        self.assertEqual('Create a Grade', add_grade_header.text)

        # Add a name
        assignment_name_input = self.browser.find_element_by_id('grade_name')
        assignment_name_input.send_keys('new test assignment')

        # Add a score
        score_input = self.browser.find_element_by_id('grade_score')
        score_input.send_keys('20')

        # Add a standard
        standard_selector = Select(self.browser.find_element_by_id('standards'))
        standard_selector.select_by_value('10')

        # Submit without adding a grade type.
        submit_button = self.browser.find_element_by_xpath("//input[@type='submit']")
        submit_button.click()

        # Make sure we're still on the create grade page.
        add_grade_header = self.browser.find_element_by_tag_name('h1')
        self.assertEqual('Create a Grade', add_grade_header.text)

        # Find the error for the grade type.
        grade_type_error = self.browser.find_element_by_id('grade_type__error')
        self.assertIsNotNone(grade_type_error)
        self.assertEqual('Value not in database', grade_type_error.text)

    def test_teacher_add_new_assignment_requires_score(self):
        self.browser.get(self.server_url)

        self.log_in() # Gradebook
        self.browser.find_element_by_link_text('Math One')

        # Navigate directly to the new assignment page.
        self.browser.get(self.server_url + 'grades/create/2/2')

        # Make sure we're on the create grade page.
        add_grade_header = self.browser.find_element_by_tag_name('h1')
        self.assertEqual('Create a Grade', add_grade_header.text)

        # Add a name
        assignment_name_input = self.browser.find_element_by_id('grade_name')
        assignment_name_input.send_keys('new test assignment')

        # Add a grade type
        grade_type_selector = Select(self.browser.find_element_by_id('grade_grade_type'))
        grade_type_selector.select_by_visible_text('Assignment')

        # Add a standard
        standard_selector = Select(self.browser.find_element_by_id('standards'))
        standard_selector.select_by_value('10')

        # Submit without adding a grade type.
        submit_button = self.browser.find_element_by_xpath("//input[@type='submit']")
        submit_button.click()

        # Make sure we're still on the create grade page.
        add_grade_header = self.browser.find_element_by_tag_name('h1')
        self.assertEqual('Create a Grade', add_grade_header.text)

        # Find the error for the grade type.
        score_error = self.browser.find_element_by_id('score__error')
        self.assertIsNotNone(score_error)
        self.assertEqual('Enter a number greater than or equal to 0', score_error.text)
