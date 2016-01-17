import unittest
import cPickle as pickle
from gluon import * 
from gluon import current
from globals import Request
from gluon.shell import *

class GradeBookController(unittest.TestCase):

    def setUp(self):
        #self.env = new_env(app='student_growth_tracker', controller='gradebook')
        #request = Request(self.env)
        #env = exec_environment('applications/student_growth_tracker/models/db.py')
        #request = Request(env)
        #db = test_db
        execfile("applications/student_growth_tracker/controllers/gradebook.py", globals())
        auth.user = Storage(dict(id=2))
        
        
    def test_index(self):   
        #resp = response.render(vars)
        #request.post_vars["id"] = 2
        #request.controller = 'gradebook'
        #request.function = 'index'
        #db = test_db
        resp = index()
        print(resp)
        self.assertEquals(resp["class_data"][0][0], "Math One")
        self.assertEquals(resp["class_data"][0][2], "Mathematics")
        self.assertEquals(resp["class_data"][0][3], "79.05")
        self.assertEquals(resp["class_data"][1][0], "Math Two")
        self.assertEquals(resp["class_data"][1][2], "Mathematics")
        self.assertEquals(resp["class_data"][1][3], "76.67")

