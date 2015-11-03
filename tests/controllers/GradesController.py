import unittest
from gluon.globals import Request, Session, Storage, Response
from gluon import current


class GradesController(unittest.TestCase):
    def setUp(self):
        self.request = current.request
        self.controller = execfile("applications/student_growth_tracker/controllers/grades.py", globals())
        

    #Not fully working example
    def test_create(self):
        request.args=[2]
        resp = create()
        self.request.function = 'create'
        self.request._post_vars = Storage({
            'name': 'unit',
            'display_date': '2015-11-2',
            'date_assigned': '2015-11-2',
            'due_date': '2015-11-2',
            'score': 2,
            'isPassFail': False,
            '_formkey': resp['form'].formkey,
            '_formname': resp['form'].formname
            })
        
        try:
            
            create()

        except Exception:
            self.fail("In exception")

        
        

    def test_grades_two(self):
        self.assertEqual('boo'.upper(), 'BOO')

