import unittest
import cPickle as pickle
from gluon import * 
from gluon import current
from globals import Request
from gluon.shell import *

class StudentController(unittest.TestCase):
    def setUp(self):
        execfile("applications/student_growth_tracker/controllers/students.py", globals())
        auth.user = Storage(dict(id=3))
        #auth.membership = 3
        #auth.login_bare("bwash","test")
        #auth_user.id = Storage(dict(id=2))
        env = exec_environment('applications/student_growth_tracker/models/db.py')
        request = Request(env)
        

    def test_overview(self):        

        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        request.function = "overview"

        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("Student" + request.function)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

        resp = overview()
        print("************************************")
        print("")
        print(resp)
        print("************************************")
        self.assertEquals(resp['name'], "Student One")
        self.assertEquals(resp['overview_data'][1][0], "Language Arts One")
        self.assertEquals(resp['overview_data'][1][1], "74.21")
        self.assertEquals(resp['overview_data'][2][0], "Math One")
        self.assertEquals(resp['overview_data'][2][1], "76.19")
