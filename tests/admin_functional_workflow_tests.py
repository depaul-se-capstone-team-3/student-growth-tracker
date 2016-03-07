import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select


USERNAME = 'Admin_One'
PASSWORD = 'test'


class AdminFunctionalWorkflowTest(unittest.TestCase):

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

    def test_admin_can_log_in(self):
        self.browser.get(self.server_url)

        self.log_in()

        header = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Admin Tools', header)

    def test_class_workflow(self):
        self.browser.get(self.server_url)

        self.log_in()

        #CLASS LIST TEST BEGINS
        #select Class List link and make sure we get to the right page.
        self.browser.find_element_by_id('classes_list').click()
        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Classes List', header)
        #make sure there's a return in the test data
        class_container = self.browser.find_element_by_id('class_list_table')
        self.assertIsNotNone(class_container)
        table_rows = class_container.find_elements_by_tag_name('tr')
        #check that the right number of classes return
        self.assertEqual(len(table_rows), 4)
        #verify display data
        row_list = table_rows[1].find_elements_by_tag_name('td')
        self.assertEquals(row_list[0].text, '7')
        self.assertEquals(row_list[1].text, 'Language Arts')
        self.assertEquals(row_list[2].text, 'Language Arts One')
        self.assertEquals(row_list[3].text, 'Bob Johnson')
        
        row_list = table_rows[2].find_elements_by_tag_name('td')
        self.assertEquals(row_list[0].text, '7')
        self.assertEquals(row_list[1].text, 'Mathematics')
        self.assertEquals(row_list[2].text, 'Math One')
        self.assertEquals(row_list[3].text, 'Ted Whitrock')

        #TEACHER LIST TEST BEGINS
        self.browser.find_element_by_link_text('Student Growth Tracker').click()
        self.browser.find_element_by_id('teacher_list').click()
        #select Teacher List link and make sure we get to the right page.
        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Teacher List', header)
        #make sure expected data returns
        teacher_container = self.browser.find_element_by_id('teacher_list_table')
        self.assertIsNotNone(teacher_container)
        table_rows = teacher_container.find_elements_by_tag_name('tr')
        #check that the right number of teachers return
        self.assertEqual(len(table_rows), 3)
        #check that correct information is returning in the table
        row_list = table_rows[1].find_elements_by_tag_name('td')
        self.assertEquals(row_list[0].text, 'Bob Johnson')
        self.assertEquals(row_list[1].text, 'bobjohnson')
        self.assertEquals(row_list[2].text, 'bob.johnson@example.com')

        #STUDENT LIST TEST BEGINS
        self.browser.find_element_by_link_text('Student Growth Tracker').click()
        self.browser.find_element_by_id('student_list').click()
        #select Student List link and make sure we get to the right page.
        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Student List', header)
        #make sure expected data returns
        student_container = self.browser.find_element_by_id('student_list_table')
        self.assertIsNotNone(student_container)
        table_rows = student_container.find_elements_by_tag_name('tr')
        #check that the right number of students return
        self.assertEqual(len(table_rows), 23)
        #check some of the data to verify sequence and returns
        row_list = table_rows[1].find_elements_by_tag_name('td')
        self.assertEquals(row_list[0].text, '1001')
        self.assertEquals(row_list[1].text, 'Student One')
        self.assertEquals(row_list[2].text, 'Student_One')

        row_list = table_rows[10].find_elements_by_tag_name('td')
        self.assertEquals(row_list[0].text, '1010')
        self.assertEquals(row_list[1].text, 'Student Ten')
        self.assertEquals(row_list[2].text, 'Student_Ten')

        #PARENT LIST TEST BEGINS
        #select home, then Parent List link and make sure we get to the right page.
        self.browser.find_element_by_link_text('Student Growth Tracker').click()
        self.browser.find_element_by_id('parent_list').click()
        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Parent List', header)
        #make sure something returns with data
        parent_container = self.browser.find_element_by_id('parent_list_table')
        self.assertIsNotNone(parent_container)
        table_rows = parent_container.find_elements_by_tag_name('tr')
        #check that there is only a single parent returning
        self.assertEqual(len(table_rows), 2)

        row_list = table_rows[1].find_elements_by_tag_name('td')
        self.assertEquals(row_list[0].text, 'Parent One')
        self.assertEquals(row_list[1].text, 'Parent_One')
        self.assertEquals(row_list[2].text, 'ParentOne@gmail.com')

        #TEACHER-CLASS RELATION TEST BEGINS
        self.browser.find_element_by_link_text('Student Growth Tracker').click()        
        self.browser.find_element_by_id('teacher_class_list').click()

        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Teacher - Class Relation', header)
        
        teacher_class_container = self.browser.find_element_by_id('teacher_class_table')
        self.assertIsNotNone(teacher_class_container)
        table_rows = teacher_class_container.find_elements_by_tag_name('tr')
        #check that the right number of teachers returns
        self.assertEqual(len(table_rows), 3)

        row_list = table_rows[1].find_elements_by_tag_name('td')
        self.assertEquals(row_list[0].text, 'Bob Johnson')
        self.assertEquals(row_list[1].text, '7')
        self.assertEquals(row_list[2].text, 'Language Arts One')

        row_list = table_rows[2].find_elements_by_tag_name('td')
        self.assertEquals(row_list[0].text, 'Ted Whitrock')
        self.assertEquals(row_list[1].text, '7')
        #multi-value returns are delimited with "\n"
        self.assertEquals(row_list[2].text, 'Math One\nMath Two')

        #STUDENT-CLASS RELATION TEST BEGINS
        self.browser.find_element_by_link_text('Student Growth Tracker').click()
        self.browser.find_element_by_id('student_class_list').click()

        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Student - Class Relation', header)

        student_class_container = self.browser.find_element_by_id('student_class_table')
        self.assertIsNotNone(student_class_container)
        table_rows = student_class_container.find_elements_by_tag_name('tr')
        #check that there are 22 students returning (22 rows plus headers)
        self.assertEqual(len(table_rows), 23)
        #check some of the returns to verify sequence
        row_list = table_rows[1].find_elements_by_tag_name('td')
        self.assertEquals(row_list[0].text, 'Student One')
        self.assertEquals(row_list[1].text, '1001')
        self.assertEquals(row_list[2].text, 'Language Arts One\nMath One')       

        row_list = table_rows[9].find_elements_by_tag_name('td')
        self.assertEquals(row_list[0].text, 'Student Nine')
        self.assertEquals(row_list[1].text, '1009')
        self.assertEquals(row_list[2].text, 'Language Arts One\nMath One')

        row_list = table_rows[22].find_elements_by_tag_name('td')
        self.assertEquals(row_list[0].text, 'Student Twentytwo')
        self.assertEquals(row_list[1].text, '1022')
        self.assertEquals(row_list[2].text, 'Math Two')

        #PARENT-STUDENT RELATION TEST BEGINS
        self.browser.find_element_by_link_text('Student Growth Tracker').click()
        self.browser.find_element_by_id('parent_student_list').click()

        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Parent - Student Relation', header)

        parent_student_container = self.browser.find_element_by_id('parent_student_table')
        self.assertIsNotNone(parent_student_container)
        table_rows = parent_student_container.find_elements_by_tag_name('tr')
        #check that there is a single base Parent to Student relationship
        self.assertEqual(len(table_rows), 2)

        row_list = table_rows[1].find_elements_by_tag_name('td')
        self.assertEquals(row_list[0].text, 'Parent One')
        #multi-value returns are delimited with "\n"
        self.assertEquals(row_list[1].text, 'Student One\nStudent Two')         

        #ADD TEACHER TEST BEGINS
        self.browser.find_element_by_link_text('Student Growth Tracker').click()        
        self.browser.find_element_by_id('teacher_create').click()
        
        #Enter the various information fields for adding a new teacher
        teacher_name_input = self.browser.find_element_by_id('no_table_first_name')
        teacher_name_input.send_keys('Wilhelm')

        teacher_name_input = self.browser.find_element_by_id('no_table_last_name')
        teacher_name_input.send_keys('von Richtenstein')

        teacher_email_input = self.browser.find_element_by_id('no_table_email')
        teacher_email_input.send_keys('WillyVonRichter@email.com')

        teacher_username_input = self.browser.find_element_by_id('no_table_username')
        teacher_username_input.send_keys('WillyV')

        teacher_password_input = self.browser.find_element_by_id('no_table_password')
        teacher_password_input.send_keys('test')

        #submit changes
        submit_button = self.browser.find_element_by_xpath("//input[@type='submit']")
        submit_button.click()

        #check that the newly added teacher is in the database
        self.browser.find_element_by_link_text('Student Growth Tracker').click()
        self.browser.find_element_by_id('teacher_list').click()

        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Teacher List', header)
        teacher_container = self.browser.find_element_by_id('teacher_list_table')
        self.assertIsNotNone(teacher_container)
        table_rows = teacher_container.find_elements_by_tag_name('tr')
        self.assertEqual(len(table_rows), 4)
        row_list = table_rows[3].find_elements_by_tag_name('td')
        self.assertEquals(row_list[0].text, 'Wilhelm von Richtenstein')
        self.assertEquals(row_list[1].text, 'WillyV')
        self.assertEquals(row_list[2].text, 'WillyVonRichter@email.com')

        #ADD CLASS TEST BEGINS
        self.browser.find_element_by_link_text('Student Growth Tracker').click()      
        self.browser.find_element_by_id('classes_create').click()
        
        #Enter the various information fields for adding a new class
        class_name_input = self.browser.find_element_by_id('no_table_name')
        class_name_input.send_keys('new test class')

        grade_level_input = self.browser.find_element_by_id('no_table_grade_level')
        grade_level_input.send_keys('8')

        start_date_input = self.browser.find_element_by_id('no_table_start_date')
        start_date_input.clear()
        start_date_input.send_keys('2016-01-25 00:00:00')

        end_date_input = self.browser.find_element_by_id('no_table_end_date')
        end_date_input.clear()
        end_date_input.send_keys('2016-04-25 00:00:00')
        
        content_area_selector = Select(self.browser.find_element_by_id('no_table_content_area'))
        content_area_selector.select_by_value('1')

        submit_button = self.browser.find_element_by_xpath("//input[@type='submit']")
        submit_button.click()

        #check that newly added class is in the database
        self.browser.find_element_by_link_text('Student Growth Tracker').click()
        self.browser.find_element_by_id('classes_list').click()        
        class_container = self.browser.find_element_by_id('class_list_table')
        self.assertIsNotNone(class_container)
        table_rows = class_container.find_elements_by_tag_name('tr')
        
        #ADD STUDENT TEST BEGINS
        self.browser.find_element_by_link_text('Student Growth Tracker').click()        
        self.browser.find_element_by_id('student_create').click()

        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Create Student', header)
        #Enter the various information fields for adding a new student
        student_first_name_input = self.browser.find_element_by_id('no_table_first_name')
        student_first_name_input.send_keys('Test')
        
        student_last_name_input = self.browser.find_element_by_id('no_table_last_name')
        student_last_name_input.send_keys('Student')

        student_email_input = self.browser.find_element_by_id('no_table_email')
        student_email_input.send_keys('TestStudent@email.com')

        student_username_input = self.browser.find_element_by_id('no_table_username')
        student_username_input.send_keys('Test_Student')

        student_password_input = self.browser.find_element_by_id('no_table_password')
        student_password_input.send_keys('test')

        student_id_number_input = self.browser.find_element_by_id('no_table_School_ID_Number')
        student_id_number_input.send_keys('2001')

        student_grade_input = self.browser.find_element_by_id('no_table_Grade_Level')
        student_grade_input.send_keys('8')

        submit_button = self.browser.find_element_by_xpath("//input[@type='submit']")
        submit_button.click()

        #ADD STUDENT TO CLASS
        self.browser.find_element_by_link_text('Student Growth Tracker').click()       
        self.browser.find_element_by_id('assign_student').click()
        
        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Assign Student to Class', header)

        student_selector = Select(self.browser.find_element_by_id('no_table_Student'))
        student_selector.select_by_value('23')

        class_selector = Select(self.browser.find_element_by_id('no_table_Class'))
        class_selector.select_by_value('4')

        submit_button = self.browser.find_element_by_xpath("//input[@type='submit']")
        submit_button.click()

        #Check that student is in the database
        self.browser.find_element_by_link_text('Student Growth Tracker').click()
        self.browser.find_element_by_id('student_list').click()

        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Student List', header)

        student_container = self.browser.find_element_by_id('student_list_table')
        self.assertIsNotNone(student_container)
        table_rows = student_container.find_elements_by_tag_name('tr')
        #check that the new student is where we expect it.
        row_list = table_rows[23].find_elements_by_tag_name('td')
        self.assertEquals(row_list[0].text, '2001')
        self.assertEquals(row_list[1].text, 'Test Student')
        self.assertEquals(row_list[2].text, 'Test_Student')

        #ADD PARENT TEST BEGINS
        self.browser.find_element_by_link_text('Student Growth Tracker').click()
        self.browser.find_element_by_id('parent_create').click()
        
        #Enter the various information fields for adding a new parent
        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Create Parent', header)

        parent_first_name_input = self.browser.find_element_by_id('no_table_first_name')
        parent_first_name_input.send_keys('Test')

        parent_last_name_input = self.browser.find_element_by_id('no_table_last_name')
        parent_last_name_input.send_keys('Parent')

        parent_email_input = self.browser.find_element_by_id('no_table_email')
        parent_email_input.send_keys('TestParent@gmail.com')

        parent_username_input = self.browser.find_element_by_id('no_table_username')
        parent_username_input.send_keys('Test_Parent')

        parent_password_input = self.browser.find_element_by_id('no_table_password')
        parent_password_input.send_keys('test')

        submit_button = self.browser.find_element_by_xpath("//input[@type='submit']")
        submit_button.click()

        self.browser.find_element_by_link_text('Student Growth Tracker').click()
        self.browser.find_element_by_id('parent_list').click()

        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Parent List', header)

        parent_container = self.browser.find_element_by_id('parent_list_table')
        self.assertIsNotNone(parent_container)
        table_rows = parent_container.find_elements_by_tag_name('tr')
        #check that there are two parents in the table now
        self.assertEqual(len(table_rows), 3)
        #check that the information added is the information returned
        row_list = table_rows[2].find_elements_by_tag_name('td')
        self.assertEquals(row_list[0].text, 'Test Parent')
        self.assertEquals(row_list[1].text, 'Test_Parent')
        self.assertEquals(row_list[2].text, 'TestParent@gmail.com')

        #ASSIGN TEACHER TO CLASS TEST BEGINS
        self.browser.find_element_by_link_text('Student Growth Tracker').click()        
        self.browser.find_element_by_id('assign_teacher').click()

        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Assign Teacher to Class', header)

        teacher_selector = Select(self.browser.find_element_by_id('no_table_Teacher'))
        teacher_selector.select_by_value('27')

        class_selector = Select(self.browser.find_element_by_id('no_table_Class'))
        class_selector.select_by_value('4')

        submit_button = self.browser.find_element_by_xpath("//input[@type='submit']")
        submit_button.click()
        
        self.browser.find_element_by_link_text('Student Growth Tracker').click()
        self.browser.find_element_by_id('teacher_class_list').click()

        header = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Teacher - Class Relation', header)
        
        teacher_class_container = self.browser.find_element_by_id('teacher_class_table')
        self.assertIsNotNone(teacher_class_container)
        table_rows = teacher_class_container.find_elements_by_tag_name('tr')
        #check that there are now three teachers returning
        self.assertEqual(len(table_rows), 4)
        #check that new teacher (WillyV) is in the database
        row_list = table_rows[3].find_elements_by_tag_name('td')
        self.assertEquals(row_list[0].text, 'Wilhelm von Richtenstein')
        self.assertEquals(row_list[1].text, '8')
        self.assertEquals(row_list[2].text, 'new test class')

        #ASSIGN PARENT TO STUDENT TEST BEGINS
        self.browser.find_element_by_link_text('Student Growth Tracker').click()
        self.browser.find_element_by_id('assign_parent').click()      

        parent_selector = Select(self.browser.find_element_by_id('no_table_Parent'))
        parent_selector.select_by_value('29')

        student_selector = Select(self.browser.find_element_by_id('no_table_Student'))
        student_selector.select_by_value('23')

        submit_button = self.browser.find_element_by_xpath("//input[@type='submit']")
        submit_button.click()

        self.browser.find_element_by_link_text('Student Growth Tracker').click()
        self.browser.find_element_by_id('parent_student_list').click()

        parent_student_container = self.browser.find_element_by_id('parent_student_table')
        self.assertIsNotNone(parent_student_container)
        table_rows = parent_student_container.find_elements_by_tag_name('tr')
        #check that there is an updated Parent Student relationship
        self.assertEqual(len(table_rows), 3)

        row_list = table_rows[2].find_elements_by_tag_name('td')
        self.assertEquals(row_list[0].text, 'Test Parent')
        self.assertEquals(row_list[1].text, 'Test Student')    
