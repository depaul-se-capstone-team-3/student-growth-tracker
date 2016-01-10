import unittest
from gluon.globals import Request, Session, Storage, Response
from gluon import current


class GradesController(unittest.TestCase):
    def setUp(self):
        self.request = current.request
        self.controller = execfile("applications/student_growth_tracker/controllers/grades.py", globals())
        

    #Not fully working example
    def test_create(self):
        self.assertEqual('boo'.upper(), 'BOO')

    def test_grades_two(self):
        self.assertEqual('boo'.upper(), 'BOO')

