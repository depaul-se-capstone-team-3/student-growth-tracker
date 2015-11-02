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

    student_id = db.auth_user.insert(first_name='Bradford',last_name='Washington',
                                     username='bwash',
                                     email='brad.washington@email.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(STUDENT), student_id)
    
    student_id = db.auth_user.insert(first_name='Gwen',last_name='Holmes',
                                     username='gholmes',
                                     email='gwen.holmes@email.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(STUDENT), student_id)

    student_id = db.auth_user.insert(first_name='Cary',last_name='Erickson',
                                     username='cerickson',
                                     email='cary.erickson@email.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(STUDENT), student_id)
    
    student_id = db.auth_user.insert(first_name='Kelly',last_name='Horton',
                                     username='khorton',
                                     email='kelly.horton@email.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(STUDENT), student_id)
    
    student_id = db.auth_user.insert(first_name='Manuel',last_name='Jordan',
                                     username='mjordan',
                                     email='manuel.jordan@email.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(STUDENT), student_id)
    
    student_id = db.auth_user.insert(first_name='Garry',last_name='James',
                                     username='gjames',
                                     email='garry.james@email.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(STUDENT), student_id)
    
    student_id = db.auth_user.insert(first_name='Frankie',last_name='Morales',
                                     username='fmorales',
                                     email='frankie.morales@email.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(STUDENT), student_id)
    
    student_id = db.auth_user.insert(first_name='Douglas',last_name='Sullivan',
                                     username='dsullivan',
                                     email='douglas.sullivan@email.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(STUDENT), student_id)
    
    student_id = db.auth_user.insert(first_name='Mable',last_name='Estrada',
                                     username='mestrada',
                                     email='mable.estrada@email.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(STUDENT), student_id)
    
    student_id = db.auth_user.insert(first_name='Doug',last_name='Jiminez',
                                     username='djiminez',
                                     email='doug.jiminez@email.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(STUDENT), student_id)
    
    student_id = db.auth_user.insert(first_name='Jill',last_name='Thompson',
                                     username='jthompson',
                                     email='jill.thompson@email.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(STUDENT), student_id)
    
    student_id = db.auth_user.insert(first_name='Jose',last_name='Hicks',
                                     username='jhicks',
                                     email='jose.hicks@email.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(STUDENT), student_id)
    
    student_id = db.auth_user.insert(first_name='Debbie',last_name='Walsh',
                                     username='dwalsh',
                                     email='debbie.walsh@email.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(STUDENT), student_id)
    
    student_id = db.auth_user.insert(first_name='Brenda',last_name='Romero',
                                     username='bromero',
                                     email='brenda.romero@email.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(STUDENT), student_id)
    
    student_id = db.auth_user.insert(first_name='Cecil',last_name='Doyle',
                                     username='cdoyle',
                                     email='cecil.doyle@email.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(STUDENT), student_id)
    
    student_id = db.auth_user.insert(first_name='Lucas',last_name='Diaz',
                                     username='ldiaz',
                                     email='lucaz.diaz@email.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(STUDENT), student_id)
    
    student_id = db.auth_user.insert(first_name='Heidi',last_name='Payne',
                                     username='hpayne',
                                     email='heidi.payne@email.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(STUDENT), student_id)
    
    student_id = db.auth_user.insert(first_name='Estelle',last_name='Cobb',
                                     username='ecobb',
                                     email='estelle.cobb@email.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(STUDENT), student_id)
    
    student_id = db.auth_user.insert(first_name='Marshall',last_name='Dawson',
                                     username='mdawson',
                                     email='marshall.dawson@email.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(STUDENT), student_id)

    student_id = db.auth_user.insert(first_name='Marilyn',last_name='Yates',
                                     username='myates',
                                     email='marilyn.yates@email.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(STUDENT), student_id)
    
    student_id = db.auth_user.insert(first_name='Sam',last_name='Park',
                                     username='spark',
                                     email='sam.park@email.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(STUDENT), student_id)
    
    student_id = db.auth_user.insert(first_name='Eunice',last_name='Hansen',
                                     username='ehansen',
                                     email='eunice.hansen@email.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(STUDENT), student_id)
    
    student_id = db.auth_user.insert(first_name='Virgil',last_name='Burgess',
                                     username='vburgess',
                                     email='virgil.burgess@email.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(STUDENT), student_id)
    
    student_id = db.auth_user.insert(first_name='Julius',last_name='Glover',
                                     username='jglover',
                                     email='julius.glover@email.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(STUDENT), student_id)
    
    student_id = db.auth_user.insert(first_name='Derrick',last_name='Casey',
                                     username='dcasey',
                                     email='derrick.casey@email.com',
                                     password=CRYPT()('test')[0])
    auth.add_membership(auth.id_group(STUDENT), student_id)
    
# Add the default grade types.
if db(db.grade_type).isempty():
    db.grade_type.insert(name='Assignment',
                         description='Homework, projects, stuff like that')
    db.grade_type.insert(name='Assessment',
                         description='Tests, quzzes, etc.')

# Load the rest of the test data.
path = None

# This should be updated to use actual paths.
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

    if db(db.student_grade).isempty():
        path = DATA_PATH_PATTERN % (12, 'student_grade')
        db.student_grade.import_from_csv_file(open(path, 'r'))

except Exception, e:
    response.flash = '%s: loading %s' % (e, path)
