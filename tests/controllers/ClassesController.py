import unittest
from gluon import * 
from gluon import current
from globals import Request
from gluon.shell import *

class ClassesController(unittest.TestCase):
    def setUp(self):
        execfile("applications/student_growth_tracker/controllers/classes.py", globals())
        auth.user = Storage(dict(id=2))

        env = exec_environment('applications/student_growth_tracker/models/db.py')
        request = Request(env)
        

    def test_overview(self):        

        request.function = "overview"
        request.args.append(3)

        resp = overview()

        # Test basic values for the class being returned
        self.assertEquals(resp["class_name"], "Math Two")
        self.assertEquals(resp["total_students"], 12)
        self.assertEquals(resp["total_grades"], 16)
        self.assertEquals(resp["average"], 76.67)

        # Test the returns coming back in the standards dictionary, along with averages
        self.assertEquals(resp["standard_dict"][8L][2], "7.M.3")
        self.assertEquals(resp["standard_dict"][8L][3], "Math Standard Three")
        standard_average = resp["standard_dict"][8L][1]/resp["standard_dict"][8L][0]
        standard_average = round(standard_average, 4)
        self.assertEquals(standard_average * 100, 77.50)
        self.assertEquals(resp["standard_dict"][9L][2], "7.M.4")
        self.assertEquals(resp["standard_dict"][9L][3], "Math Standard Four")
        standard_average = resp["standard_dict"][9L][1]/resp["standard_dict"][9L][0]
        standard_average = round(standard_average, 4)
        self.assertEquals(standard_average * 100, 76.67)

        # Test Due Soon
        self.assertEquals(resp["due_soon_amount"], 0)
