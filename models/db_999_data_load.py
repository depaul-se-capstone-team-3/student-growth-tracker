"""
A script for loading dummy data into the database.

Manual loading is hard.

This module is for testing only. It should be removed or disabled before
migrating to Production.
"""

import os.path

NUM_STUDENTS = 10
ADMIN = 'Administrator'
TEACHER = 'Teacher'
STUDENT = 'Student'
PARENT = 'Parent'
DATA_PATH_PATTERN = os.path.join(request.folder, 'private',
                                 'dummy_files/load_%02d_db_%s_dummy.csv')

# Add our default roles.
if db(db.auth_group).isempty():
    auth.add_group(ADMIN, ADMIN)
    auth.add_group(TEACHER, TEACHER)
    auth.add_group(STUDENT, STUDENT)
    auth.add_group(PARENT, PARENT)

auth.settings.everybody_group_id = auth.id_group(TEACHER)

# Add some users - two eachers and NUM_STUDENTS students.
if db(db.auth_user).isempty():
    import datetime
    from gluon.contrib.populate import populate
    teacher_id = db.auth_user.insert(first_name='Bob',last_name='Johnson',
                                     username='bobjohnson',
                                     email='bob.johnson@example.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(TEACHER), teacher_id)
    
    teacher_id = db.auth_user.insert(first_name='Ted',last_name='Whitrock',
                                     username='tedwhitrock',
                                     email='ted.whitrock@example.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(TEACHER), teacher_id)

    for s in range(NUM_STUDENTS):
        st_id = db.auth_user.insert(first_name='Stu',last_name='Dent{}'.format(s),
                                    username='student{}'.format(s),
                                    email='student{}@example.com'.format(s),
                                    password=CRYPT()('test')[0])
        auth.add_membership(auth.id_group(STUDENT), st_id)

# Add the default grade types.
if db(db.grade_type).isempty():
    db.grade_type.insert(name='Assignment',
                         description='Homework, projects, stuff like that')
    db.grade_type.insert(name='Assessment',
                         description='Tests, quzzes, etc.')

# Load the rest of the test data.
path = None

try:
    if db(db.contentarea).isempty():
        path = DATA_PATH_PATTERN % (20, 'contentarea')
        db.contentarea.import_from_csv_file(open(path, 'r'))

    if db(db.standard).isempty():
        path = DATA_PATH_PATTERN % (25, 'standard')
        db.standard.import_from_csv_file(open(path, 'r'))

    if db(db.classes).isempty():
        path = DATA_PATH_PATTERN % (30, 'classes')
        db.classes.import_from_csv_file(open(path, 'r'))

    if db(db.gradebook).isempty():
        path = DATA_PATH_PATTERN % (40, 'gradebook')
        db.gradebook.import_from_csv_file(open(path, 'r'))

    if db(db.grade).isempty():
        path = DATA_PATH_PATTERN % (50, 'grade')
        db.grade.import_from_csv_file(open(path, 'r'))

    if db(db.grade_standard).isempty():
        path = DATA_PATH_PATTERN % (51, 'grade_standard')
        db.grade_standard.import_from_csv_file(open(path, 'r'))

    if db(db.class_grade).isempty():
        path = DATA_PATH_PATTERN % (52, 'class_grade')
        db.class_grade.import_from_csv_file(open(path, 'r'))

    if db(db.student).isempty():
        path = DATA_PATH_PATTERN % (60, 'student')
        db.student.import_from_csv_file(open(path, 'r'))

    if db(db.student_classes).isempty():
        path = DATA_PATH_PATTERN % (61, 'student_classes')
        db.student_classes.import_from_csv_file(open(path, 'r'))

except Exception, e:
    response.flash = '%s: loading %s' % (e, path)
