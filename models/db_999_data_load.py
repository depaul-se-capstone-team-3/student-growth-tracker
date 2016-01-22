"""
A script for loading demo data into the database.

This module is for testing only. It should be removed or disabled before
migrating to Production.
"""

import glob
import os.path
import os
import re

ADMIN = 'Administrator'
TEACHER = 'Teacher'
STUDENT = 'Student'
PARENT = 'Parent'

# Add our default roles.
if db(db.auth_group).isempty():
    auth.add_group(ADMIN, ADMIN)
    auth.add_group(TEACHER, TEACHER)
    auth.add_group(STUDENT, STUDENT)
    auth.add_group(PARENT, PARENT)
    
# Add the default grade types.
if db(db.grade_type).isempty():
    db.grade_type.insert(name='Assignment',
                         description='Homework, projects, stuff like that')
    db.grade_type.insert(name='Assessment',
                         description='Tests, quzzes, etc.')

# Load the demo data.

file_name_pattern = re.compile(r'\d+_(?P<dbname>.+).csv')

original_directory = os.path.abspath('.')
demo_data_path = os.path.join(original_directory,
                              'applications/student_growth_tracker/private/demo_data')

os.chdir(demo_data_path)

try:
    for import_file in glob.glob(r'*.csv'):
        match = file_name_pattern.match(import_file)
        if match:
            table_name = match.group('dbname')
            if db(db[table_name]).isempty():
                db[table_name].import_from_csv_file(open(import_file, 'r'))
except Exception as e:
    pass

os.chdir(original_directory)

if __name__ == '__main__':
    pass
