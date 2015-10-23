# -*- coding: utf-8 -*-
# try something like


def index():
    #constraints = db.gradebook.teacher == auth.user.id
    #grid = SQLFORM.smartgrid(db.grade)

    #grid = db(db.grade.name).select(join=db.grade.on((db.grade.name==db.student_grade.grade_id)))
    
    grid = db().select(db.grade.id, db.grade.name, db.grade.display_date, db.grade.date_assigned, db.grade.due_date,db.grade.grade_type,db.grade.score, db.grade.isPassFail)
    return dict(grid=grid)


def create():
    form = SQLFORM(db.grade).process(next=URL('index'))
    return dict(form=form)


def query():
    gname = request.vars['gname']
    assignment = db.student_grade.grade_id==gname
    c1 = (db.student.user_id== db.auth_user.id) & (db.grade.id == db.student_grade.grade_id)
    grade_query = db(assignment).select(db.auth_user.id,db.auth_user.first_name,db.auth_user.last_name, db.student_grade.student_score, left=db.student_grade.on(c1))
    return dict(grade_query=grade_query)
