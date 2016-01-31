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
        env = exec_environment('applications/student_growth_tracker/models/db.py')
        request = Request(env)
        

    def test_overview(self):        

        request.function = "overview"

        resp = overview()

        self.assertEquals(resp['name'], "Student One")
        self.assertEquals(resp['overview_data'][1][0], "Language Arts One")
        self.assertEquals(resp['overview_data'][1][1], "74.21")

        # Due_list to be tested with data later.
        row = resp['overview_data'][1][2]
        self.assertTrue(len(row) == 1)
        
        self.assertEquals(resp['overview_data'][2][0], "Math One")
        self.assertEquals(resp['overview_data'][2][1], "76.19")

        # Due_list to be tested with data later.
        row = resp['overview_data'][2][2]
        self.assertTrue(len(row) == 1)

    def test_index(self):
        request.args.pop(0)
        request.args.append(1)
        
        resp = index()

        self.assertEquals(resp['class_name'], "Language Arts One")
        self.assertEquals(resp['name'], "Student One")
        
        self.assertEquals(resp["assignment_data"][0][0],"LA Assignment One")
        self.assertEquals(resp["assignment_data"][0][1], 10.0)
        self.assertEquals(resp["assignment_data"][0][2], 10.0)
        self.assertEquals(resp["assignment_data"][0][3], 100.0)
        self.assertEquals(resp["assignment_data"][0][4], "Dec 08, 2015")
        self.assertEquals(resp["assignment_data"][0][5], "success")

        self.assertEquals(resp["assignment_data"][1][0],"LA Assignment Two")
        self.assertEquals(resp["assignment_data"][1][1], 8.0)
        self.assertEquals(resp["assignment_data"][1][2], 10.0)
        self.assertEquals(resp["assignment_data"][1][3], 80.0)
        self.assertEquals(resp["assignment_data"][1][4], "Dec 09, 2015")
        self.assertEquals(resp["assignment_data"][1][5], "success")

        self.assertEquals(resp["assignment_data"][2][0],"LA Assignment Three")
        self.assertEquals(resp["assignment_data"][2][1], 9.0)
        self.assertEquals(resp["assignment_data"][2][2], 10.0)
        self.assertEquals(resp["assignment_data"][2][3], 90.0)
        self.assertEquals(resp["assignment_data"][2][4], "Dec 10, 2015")
        self.assertEquals(resp["assignment_data"][2][5], "success")

        self.assertEquals(resp["assignment_data"][3][0],"LA Assignment Four")
        self.assertEquals(resp["assignment_data"][3][1], 5.0)
        self.assertEquals(resp["assignment_data"][3][2], 10.0)
        self.assertEquals(resp["assignment_data"][3][3], 50.0)
        self.assertEquals(resp["assignment_data"][3][4], "Dec 11, 2015")
        self.assertEquals(resp["assignment_data"][3][5], "success")

        self.assertEquals(resp["assignment_data"][4][0],"LA Assignment Five")
        self.assertEquals(resp["assignment_data"][4][1], 7.0)
        self.assertEquals(resp["assignment_data"][4][2], 10.0)
        self.assertEquals(resp["assignment_data"][4][3], 70.0)
        self.assertEquals(resp["assignment_data"][4][4], "Dec 14, 2015")
        self.assertEquals(resp["assignment_data"][4][5], "success")


