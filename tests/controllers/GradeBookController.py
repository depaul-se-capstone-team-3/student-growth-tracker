import unittest
import cPickle as pickle
from gluon import * 
from gluon import current
from globals import Request
from gluon.shell import *
db = test_db
execfile("applications/student_growth_tracker/controllers/gradebook.py", globals())

class GradeBookController(unittest.TestCase):

    def setUp(self):
        #self.env = new_env(app='student_growth_tracker', controller='gradebook')
        #request = Request(self.env)
        env = exec_environment('applications/student_growth_tracker/models/db.py')
        request = Request(env)
        auth.user = Storage(dict(id=1))
        
        
    def test_index(self):
        #self.assertEqual('boo'.upper(), 'BOO')
        
        #resp = response.render(vars)
        request.post_vars["id"] = 2
        request.controller = 'gradebook'
        request.function = 'index'
        resp = index()
        print("--------------------------------")
        print(resp)
        print(type(resp))
        print("--------------------------------")
        
