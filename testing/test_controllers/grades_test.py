import unittest
import copy

from gluon.globals import Request

#from gluon import current
#db = DAL('sqlite://storage.sqlite')
#current.db = db

execfile("applications/student_growth_tracker/controllers/grades.py", globals())

#db = test_db
#db(db.grade.id>0).delete()
#db.commit()


#to run in command prompt, navigate to web2py folder then type the following:
#python web2py.py -S student_growth_tracker\testing\test_controllers -M -R applications\student_growth_tracker\testing\test_controllers\grades_test.py

class TestGradeCreate(unittest.TestCase):
#    def setUp(self):
#        test_db = DAL('sqlite://testing.sqlite')  # Name and location of the test DB file
#        for tablename in db.tables:  # Copy tables!
#            table_copy = [copy.copy(f) for f in db[tablename]]
#            test_db.define_table(tablename, *table_copy)

#        db = test_db
#        db(db.grade.id>0).delete()
#        db.commit()

    def test_one(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_two(self):
        self.assertEqual('boo'.upper(), 'BOO')

        
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestGradeCreate))
unittest.TextTestRunner(verbosity=2).run(suite)
