"""This module is for testing only. It should be removed or disabled before
migrating to Production."""

NUM_STUDENTS = 10

####################################################################################################
# Populate some tables so we have data with which to work.
ADMIN = 'Administrator'
TEACHER = 'Teacher'
STUDENT = 'Student'
PARENT = 'Parent'
if db(db.auth_group).isempty():
    auth.add_group(ADMIN, ADMIN)
    auth.add_group(TEACHER, TEACHER)
    auth.add_group(STUDENT, STUDENT)
    auth.add_group(PARENT, PARENT)

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


    # populate(db.auth_user,300)
    # db(db.auth_user.id>1).update(is_student=True,is_teacher=False,is_administrator=False)


    # # Add everyone in the auth_user table - except Massimo - to the student group.
    # for k in range(200,300):
    #     id = db.course.insert(name='Dummy course',
    #                           code='CSC%s' % k,
    #                           prerequisites=[],
    #                           tags=[],
    #                           description = 'description...')
    #     for s in range(701,703):
    #         i = db.course_section.insert(
    #             name='CSC%s-%s' % (k,s),
    #             course=id,
    #             meeting_place='CDM',
    #             meeting_time='Tuesday',
    #             start_date=datetime.date(2014,9,1),
    #             stop_date=datetime.date(2014,12,1),
    #             signup_deadline=datetime.date(2014,11,10))
    #         rows = db(db.auth_user).select(limitby=(0,10),orderby='<random>')
    #         db.membership.insert(course_section=i, auth_user=mdp_id, role=TEACHER)
    #         db.membership.insert(course_section=i, auth_user=st_id, role=STUDENT)

    #         for h in range(1,7):
    #             db.homework.insert(name='hw'+str(h), course_section=i,points=10, assignment_order=h)

    #         for row in rows:
    #             db.membership.insert(course_section=i, auth_user=row.id, role=STUDENT)
