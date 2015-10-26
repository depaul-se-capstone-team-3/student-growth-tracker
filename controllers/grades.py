# -*- coding: utf-8 -*-
# try something like


def index():
    #constraints = db.gradebook.teacher == auth.user.id
    #grid = SQLFORM.smartgrid(db.grade)

    #grid = db(db.grade.name).select(join=db.grade.on((db.grade.name==db.student_grade.grade_id)))
    
    grid = db().select(db.grade.id, db.grade.name, db.grade.display_date, db.grade.date_assigned, db.grade.due_date,db.grade.grade_type,db.grade.score, db.grade.isPassFail)
    return dict(grid=grid)

def query():
    gname = request.vars['gname']
    assignment = db.student_grade.grade_id==gname
    c1 = (db.student.user_id== db.auth_user.id) & (db.grade.id == db.student_grade.grade_id)
    grade_query = db(assignment).select(db.auth_user.id,db.auth_user.first_name,db.auth_user.last_name, db.student_grade.student_score, left=db.student_grade.on(c1))
    return dict(grade_query=grade_query)


#    form = SQLFORM.smartgrid(db.auth_user, linked_tables=[db.auth_membership,db.auth_group])
#    return dict(form=form)


def create():
    try:
        class_id = request.args[0]
    except:
        #Doing Nothing, need to handle.
        #redirect(URL("default","index"))
        class_id = 2

    #db.grade_type.name.requires = IS_IN_DB(db, 'grade_type.name', '%(name)s', zero=T('Choose Type'))
    gradeT = Field('grade_type', requires=IS_IN_DB(db, 'grade_type.id', '%(name)s',zero=T('Choose Grade Type')))
    form = SQLFORM.factory(db.grade.name,
                           db.grade.display_date,
                           db.grade.date_assigned,
                           db.grade.due_date, gradeT,
                           db.grade.score,
                           db.grade.isPassFail)

    #form = SQLFORM.smartgrid(db.grade, linked_tables=[db.grade_type]).process()
    if form.process().accepted:
        id = db.grade.insert(**db.grade._filter_fields(form.vars))

        #insert into class_grade db.
        db.class_grade.insert(class_id = class_id,grade_id = id)

    return dict(form=form)


def enter_grade():
    try:
        class_id = request.args[0]
    except:
        #Doing Nothing, need to handle.
        redirect(URL("default","index"))
    return locals()
