import unittest
import cPickle as pickle
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

        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        #print(request)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        #request.vars.class_id = 3
        #request.vars["teacher_id"] = 2
        #request.vars["class_id"] = 3
        request.function = "overview"
        request.args.append(3)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(request.args)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        #c = int(3)
        #request.args["class_id"] = c
        
        #request.post_vars["class_id"]=3
        #class_id = Storage(dict(id=3))
        #print(response.render(vars))
        resp = overview()
        print("************************************")
        print("")
        print(resp)
        print("************************************")
        #Test basic values for the class being returned
        self.assertEquals(resp["class_name"], "Math Two")
        self.assertEquals(resp["total_students"], 12)
        self.assertEquals(resp["total_grades"], 16)
        self.assertEquals(resp["average"], 76.67)
        #Test the returns coming back in the standards dictionary, along with averages
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
        #Test Due Soon
        self.assertEquals(resp["due_soon_amount"], 0)
        form = SQLFORM.factory(db.grade)
        form.vars.display_date = datetime.datetime.utcnow()
        form.vars.date_assigned = datetime.datetime.utcnow()
        form.vars.due_date = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        form.vars.name = "Due Date Test Assignment"
        id = db.grade.insert(**db.grade._filter_fields(form.vars))
        db.class_grade.insert(class_id = 3,grade_id = id)
        db.grade_standard.insert(grade_id = id, standard_id = form.vars.standard)
        for student in get_class_roster(2, 3):
            db.student_grade.insert(student_id=student[0], grade_id = id, student_score = 0)
        resp = overview()
        self.assertEquals(resp["due_soon_amount"], 1)
