# import unittest

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait, Select


# USERNAME = 'tedwhitrock'
# PASSWORD = 'test'

# class AttendanceFunctionalTest(unittest.TestCase):

#     def setUp(self):
#         self.browser = webdriver.Firefox()
#         self.server_url = 'http://localhost:8000/student_growth_tracker/'
#         self.browser.implicitly_wait(10)

#     def tearDown(self):
#         self.browser.quit()

#     def log_in(self):
#         uname_input = self.browser.find_element_by_id('auth_user_username')
#         uname_input.send_keys(USERNAME)
#         pwd_input = self.browser.find_element_by_id('auth_user_password')
#         pwd_input.send_keys(PASSWORD)
#         pwd_input.send_keys(Keys.ENTER)
