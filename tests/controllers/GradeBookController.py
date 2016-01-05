import unittest
from gluon.globals import Request, Session, Storage, Response
from gluon import current


class GradeBookController(unittest.TestCase):
	def setUp(self):
		self.request = current.request
		self.controller = execfile("applications/student_growth_tracker/controllers/gradebook.py", globals())
		db = test_db

		print("-------print1--------------------------------")
		print(db(db.auth_group).isempty())
		print("-------print1--------------------------------")
		auth.add_group(ADMIN, ADMIN)
    	auth.add_group(TEACHER, TEACHER)
    	auth.add_group(STUDENT, STUDENT)
    	auth.add_group(PARENT, PARENT)
    	print("-------print2--------------------------------")
    	print(db(db.auth_group).isempty())
    	print("-------print2--------------------------------")





	def test_gradebook(self):
		self.assertEqual('boo'.upper(), 'BOO')