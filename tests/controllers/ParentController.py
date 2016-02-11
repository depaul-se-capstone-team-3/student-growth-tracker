import unittest
import cPickle as pickle
from gluon import * 
from gluon import current
from globals import Request
from gluon.shell import *

class ParentController(unittest.TestCase):
    def setUp(self):
        execfile("applications/student_growth_tracker/controllers/parents.py", globals())
        #auth.user = Storage(dict(id=25))
        #auth.membership = 3
        auth.login_bare("Parent_One","test")
        #auth_user.id = Storage(dict(id=2))
        env = exec_environment('applications/student_growth_tracker/models/db.py')
        request = Request(env)
        

    def test_overview(self):        

        request.function = "overview"

        resp = overview()

        self.assertEquals(resp['parent_name'], "Parent One")
        full_dict = resp['full_dict']
        self.assertTrue(full_dict.has_key(1))
        self.assertTrue(full_dict.has_key(2))
        self.assertFalse(full_dict.has_key(3))
        class_dict_s1 = full_dict[1][1]
        class_dict_s2 = full_dict[2][1]
        self.assertTrue(class_dict_s1.has_key("Language Arts One"))
        self.assertTrue(class_dict_s1.has_key("Math One"))
        self.assertEquals(class_dict_s1["Language Arts One"][0],"77.89")
        self.assertEquals(class_dict_s1["Math One"][0],"86.67")
        self.assertTrue(class_dict_s2.has_key("Language Arts One"))
        self.assertTrue(class_dict_s2.has_key("Math One"))

        standards_dict_s1 = class_dict_s1["Language Arts One"][1]
        count = 0
        for standard in standards_dict_s1.keys():
            count += 1
        self.assertEquals(count, 5)
        #check that the totals being pulled are correct based on test assignments
        self.assertEquals(standards_dict_s1[1L][2], "7.LA.1")
        self.assertEquals(standards_dict_s1[1L][3], "LA Standard One")
        self.assertEquals(standards_dict_s1[1L][0], 120.0)
        self.assertEquals(standards_dict_s1[1L][1], 99.0)
        self.assertEquals(standards_dict_s1[2L][2], "7.LA.2")
        self.assertEquals(standards_dict_s1[2L][3], "LA Standard Two")
        self.assertEquals(standards_dict_s1[2L][0], 120.0)
        self.assertEquals(standards_dict_s1[2L][1], 95.0)
        self.assertEquals(standards_dict_s1[3L][2], "7.LA.3")
        self.assertEquals(standards_dict_s1[3L][3], "LA Standard Three")
        self.assertEquals(standards_dict_s1[3L][0], 120.0)
        self.assertEquals(standards_dict_s1[3L][1], 100.0)
        self.assertEquals(standards_dict_s1[4L][2], "7.LA.4")
        self.assertEquals(standards_dict_s1[4L][3], "LA Standard Four")
        self.assertEquals(standards_dict_s1[4L][0], 120.0)
        self.assertEquals(standards_dict_s1[4L][1], 98.0)
        self.assertEquals(standards_dict_s1[5L][2], "7.LA.5")
        self.assertEquals(standards_dict_s1[5L][3], "LA Standard Five")
        self.assertEquals(standards_dict_s1[5L][0], 110.0)
        self.assertEquals(standards_dict_s1[5L][1], 92.0)
        #sequence cannot be verified, but check that the right standards are in the dict
        self.assertTrue(standards_dict_s1.has_key(1))
        self.assertTrue(standards_dict_s1.has_key(2))
        self.assertTrue(standards_dict_s1.has_key(3))
        self.assertTrue(standards_dict_s1.has_key(4))
        self.assertTrue(standards_dict_s1.has_key(5))

        standards_dict_s1 = class_dict_s1["Math One"][1]
        count = 0
        for standard in standards_dict_s1.keys():
            count += 1
        self.assertEquals(count, 5)
        print (standards_dict_s1)
        #sequence cannot be verified, but check that the right standards are in the dict
        self.assertTrue(standards_dict_s1.has_key(6))
        self.assertTrue(standards_dict_s1.has_key(7))
        self.assertTrue(standards_dict_s1.has_key(8))
        self.assertTrue(standards_dict_s1.has_key(9))
        self.assertTrue(standards_dict_s1.has_key(10))
