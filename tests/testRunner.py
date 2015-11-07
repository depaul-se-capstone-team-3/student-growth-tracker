import unittest
import glob
import sys
import os

#To Run
#Navigate to web2py folder
#python web2py.py -S student_growth_tracker -M -R applications/student_growth_tracker/tests/testRunner.py

test_files = glob.glob("applications/student_growth_tracker/tests/*/*.py")

suite = unittest.TestSuite()
for test_file in test_files:
    execfile(str(os.path.abspath(test_file)), globals())
    suite.addTest(unittest.makeSuite(globals()[str(os.path.basename(test_file)[:-3])]))
    
unittest.TextTestRunner(verbosity=2).run(suite)
