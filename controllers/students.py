# -*- coding: utf-8 -*-
# try something like
'''
def index(): 
    grid = SQLFORM.smartgrid(db.student)
    return dict(grid=grid)
'''

def create():
    form = SQLFORM(db.student).process(next=URL('index'))
    return dict(form=form)

def index():
    student = db().select(db.student.id,db.student.user_id,db.student.school_id_number,db.student.grade_level)
    return dict(student=student)

def query():
    sid = request.vars['sid']
    student = (db.student_grade.student_id == sid )
    c1 = ((db.student.user_id== db.auth_user.id) & (db.student.id == db.student_grade.student_id))
    grade_query = db(student).select(db.auth_user.first_name,db.auth_user.last_name,db.student.user_id, db.student.school_id_number, db.student_grade.grade_id, db.student_grade.student_score, left=db.student_grade.on(c1))
    return dict(grade_query=grade_query)
