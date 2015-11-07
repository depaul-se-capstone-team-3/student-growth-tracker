import unittest
from gluon.globals import Request, Session, Storage, Response

class ClassesController(unittest.TestCase):
#    def setUp(self):
        

    def test_classes_one(self):
        self.assertEqual('fooo'.upper(), 'FOOO')
