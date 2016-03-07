import unittest
from gluon import * 
from gluon import current
from globals import Request
from gluon.shell import *

class GradeBookController(unittest.TestCase):

    def setUp(self):
        execfile("applications/student_growth_tracker/controllers/gradebook.py", globals())
        auth.user = Storage(dict(id=2))
        
        
    def test_index(self):   
        resp = index()

        self.assertEquals(resp["class_data"][0][0], "Math One")
        self.assertEquals(resp["class_data"][0][2], "Mathematics")
        self.assertEquals(resp["class_data"][0][3], "79.05")
        self.assertEquals(resp["class_data"][1][0], "Math Two")
        self.assertEquals(resp["class_data"][1][2], "Mathematics")
        self.assertEquals(resp["class_data"][1][3], "76.67")

