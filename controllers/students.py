# -*- coding: utf-8 -*-
# try something like

def create():
    '''basic create for student and redirect to index'''
    form = SQLFORM(db.student).process(next=URL('index'))
    return dict(form=form)

def index():
    '''basic index query all student if no args, will filter with given student ID'''
    # args for use in the view.
    args = False

    #If there is a argument(student id), view the particular student's assignments.
    # query is the constrain to select the given student.
    try:
        sid = sid = request.args[0]
        args = True
        query = ((db.student_grade.student_id == sid) &
                 (db.student_grade.grade_id == db.grade.id) &
                 (db.student.id == db.student_grade.student_id) &
                 (db.student.user_id == db.auth_user.id) &
                 (db.auth_user.id == db.auth_membership.user_id) &
                 (db.auth_membership.group_id == db.auth_group.id) &
                 (db.auth_group.id == 3))
    #If there is no argument, view all the students assignment.
    # query is the constrain to select all student along with all their assignment.
    #I can change this to somekind of redirect if this is not the desire behavior, just let me(Allan) know.
    except:
        query = ((db.student.id == db.student_grade.student_id) &
                 (db.student_grade.grade_id == db.grade.id) &
                 (db.student.user_id == db.auth_user.id) &
                 (db.auth_user.id == db.auth_membership.user_id) &
                 (db.auth_membership.group_id == db.auth_group.id) &
                 (db.auth_group.id == 3))
    #The actual "select" statment with the given "query" contrain from above.
    student_query = db(query).select(db.student.id,
                               db.auth_user.first_name,
                               db.auth_user.last_name,
                               db.grade.name,
                               db.student_grade.student_score)
    return dict(student_query=student_query, args=args)
