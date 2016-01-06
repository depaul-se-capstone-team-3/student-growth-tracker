import unittest
from gluon.globals import Request, Session, Storage, Response
from gluon import current


class GradeBookController(unittest.TestCase):
	def setUp(self):
		self.request = current.request
		self.controller = execfile("applications/student_growth_tracker/controllers/gradebook.py", globals())
		db = test_db

	def test_gradebook(self):
		self.assertEqual('boo'.upper(), 'BOO')
