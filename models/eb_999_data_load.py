# -*- coding: utf-8 -*-
import copy

test_db = DAL('sqlite://testing.sqlite')
for tablename in db.tables:  # Copy tables!
    table_copy = [copy.copy(f) for f in db[tablename]]
    test_db.define_table(tablename, *table_copy)
    
    NUM_STUDENTS = 10
ADMIN = 'Administrator'
TEACHER = 'Teacher'
STUDENT = 'Student'
PARENT = 'Parent'
DATA_PATH_PATTERN = os.path.join(request.folder, 'private',
                                 'dummy_files/load_%02d_db_%s_dummy.csv')

# Add our default roles.
if test_db(test_db.auth_group).isempty():
    auth.add_group(ADMIN, ADMIN)
    auth.add_group(TEACHER, TEACHER)
    auth.add_group(STUDENT, STUDENT)
    auth.add_group(PARENT, PARENT)

auth.settings.everybody_group_id = auth.id_group(TEACHER)

# Add some users - two eachers and NUM_STUDENTS students.
if test_db(test_db.auth_user).isempty():
    import datetime
    from gluon.contrib.populate import populate
    teacher_id = test_db.auth_user.insert(first_name='Bob',last_name='Johnsonson',
                                     username='bobjohnson',
                                     email='bob.johnson@example.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(TEACHER), teacher_id)

    teacher_id = test_db.auth_user.insert(first_name='Ted',last_name='Whitrock',
                                     username='tedwhitrock',
                                     email='ted.whitrock@example.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(TEACHER), teacher_id)

    try:
        if test_db(test_db.contentarea).isempty():
            path = DATA_PATH_PATTERN % (01, 'auth_user')
            test_db.auth_user.import_from_csv_file(open(path, 'r'))
        
            for i in xrange(3, 63):
                auth.add_membership(auth.id_group(STUDENT), i)

    except Exception, e:
        response.flash = '%s: loading %s' % (e, path)
    
# Add the default grade types.
if test_db(test_db.grade_type).isempty():
    test_db.grade_type.insert(name='Assignment',
                         description='Homework, projects, stuff like that')
    test_db.grade_type.insert(name='Assessment',
                         description='Tests, quzzes, etc.')

# Load the rest of the test data.
path = None

# This should be updated to use actual paths.
try:
    if test_db(test_db.contentarea).isempty():
        path = DATA_PATH_PATTERN % (20, 'contentarea')
        test_db.contentarea.import_from_csv_file(open(path, 'r'))

    if test_db(test_db.standard).isempty():
        path = DATA_PATH_PATTERN % (25, 'standard')
        test_db.standard.import_from_csv_file(open(path, 'r'))

    if test_db(test_db.classes).isempty():
        path = DATA_PATH_PATTERN % (30, 'classes')
        test_db.classes.import_from_csv_file(open(path, 'r'))

    if test_db(test_db.gradebook).isempty():
        path = DATA_PATH_PATTERN % (40, 'gradebook')
        test_db.gradebook.import_from_csv_file(open(path, 'r'))

    if test_db(test_db.grade).isempty():
        path = DATA_PATH_PATTERN % (53, 'grade')
        test_db.grade.import_from_csv_file(open(path, 'r'))

    if test_db(test_db.grade_standard).isempty():
        path = DATA_PATH_PATTERN % (51, 'grade_standard')
        test_db.grade_standard.import_from_csv_file(open(path, 'r'))

    if test_db(test_db.class_grade).isempty():
        path = DATA_PATH_PATTERN % (52, 'class_grade')
        test_db.class_grade.import_from_csv_file(open(path, 'r'))

    if test_db(test_db.student).isempty():
        path = DATA_PATH_PATTERN % (60, 'student')
        test_db.student.import_from_csv_file(open(path, 'r'))

    if test_db(test_db.student_classes).isempty():
        path = DATA_PATH_PATTERN % (61, 'student_classes')
        test_db.student_classes.import_from_csv_file(open(path, 'r'))

    if test_db(test_db.student_grade).isempty():
        path = DATA_PATH_PATTERN % (12, 'student_grade')
        test_db.student_grade.import_from_csv_file(open(path, 'r'))

except Exception, e:
    response.flash = '%s: loading %s' % (e, path)

if __name__ == '__main__':
    pass
