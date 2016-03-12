from selenium.webdriver.common.keys import Keys


from .base import FunctionalTest, STUDENT_USER_NAME, STUDENT_PASSWORD

class StudentFunctionalTest(FunctionalTest):

    username = STUDENT_USER_NAME
    password = STUDENT_PASSWORD

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

    def test_student_can_log_in(self):
        """
        Test that:

        1. The teacher can log in,
        2. The gradebook is displayed upon login.
        """
        self.browser.get(self.server_url)

        self.log_in()

        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Student One', header)

    def test_student_can_view_class_details(self):
        self.browser.get(self.server_url)

        self.log_in()

        math_one_link = self.browser.find_element_by_id('class-details-2')
        math_one_link.click()

        header = self.browser.find_element_by_tag_name('h3').text
        self.assertIn('Math One', header)
