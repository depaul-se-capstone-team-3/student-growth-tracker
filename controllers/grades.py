# -*- coding: utf-8 -*-
# try something like
import datetime

@auth.requires_login()
def index():
    #constraints = db.gradebook.teacher == auth.user.id
    #grid = SQLFORM.smartgrid(db.grade)

    #grid = db(db.grade.name).select(join=db.grade.on((db.grade.name==db.student_grade.grade_id)))
    
    grid = db().select(db.grade.id, db.grade.name, db.grade.display_date,
                       db.grade.date_assigned, db.grade.due_date,
                       db.grade.grade_type,db.grade.score, db.grade.isPassFail)
    return dict(grid=grid)

@auth.requires_login()
def query():
    gname = request.vars['gname']
    assignment = db.student_grade.grade_id==gname
    c1 = (db.student.user_id== db.auth_user.id)& (db.student.id == db.student_grade.student_id)
    grade_query = db(assignment).select(db.auth_user.id, db.auth_user.first_name, db.auth_user.last_name, db.student_grade.student_score, left=db.student_grade.on(c1))
    return dict(grade_query=grade_query)

@auth.requires(auth.has_membership(role='Teacher'), requires_login=True)
def create():
    # Generating form for creating a new assignment.
    # If there is an argument class id, check to see if
    # db.classes contains that class.
    class_id = (request.args(0) != None) and request.args(0, cast=int) or None
    if not class_id or not db.classes(class_id):
        session.flash = T('Invalid class ID: "%s"' % class_id)
        redirect(URL('default', 'index'))

    teacher_id = auth.user_id

    query = ((db.classes.id==class_id) &
             (db.classes.content_area==db.contentarea.id) &
             (db.standard.content_area==db.contentarea.id))

    # Creating the drop down menu for Standard.
    standards = db(query).select(db.standard.id,
                                 db.standard.short_name,
                                 db.standard.reference_number)

    options = []
    for row in standards:
        text = '%s - %s' % (row.reference_number, row.short_name)
        options.append(OPTION(text, _value=row.id))

    standards_menu = SELECT(options, _name='standards', _multiple='multiple',
                            _class='generic-widget form-control')

    form = SQLFORM(db.grade)
    form.insert(-1, standards_menu)

    # Processing the form
    if form.validate():
        response.flash = 'New grade created.'

        name = form.vars.name
        display_date = form.vars.display_date
        date_assigned = form.vars.date_assigned
        due_date = form.vars.due_date
        grade_type = form.vars.grade_type
        score = form.vars.score
        selected_standards = form.vars.standards

        grade_id = db.grade.insert(name=form.vars.name,
                                   display_date=form.vars.display_date,
                                   date_assigned=form.vars.date_assigned,
                                   due_date=form.vars.due_date,
                                   grade_type=form.vars.grade_type,
                                   score=form.vars.score)

        db.class_grade.insert(class_id=class_id, grade_id=grade_id)

        for standard_id in selected_standards:
            db.grade_standard.insert(grade_id=grade_id,
                                     standard_id=standard_id)

        for student in get_class_roster(teacher_id, class_id):
            db.student_grade.insert(student_id=student[0],
                                    grade_id=grade_id,
                                    student_score=0)

    return dict(form=form, standards=standards_menu)

@auth.requires_login()
def edit():
    if auth.has_membership(2, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))
    try:
        record = request.vars[0]
        form = SQLFORM(db.student_grade, record)
    except:
        record = 0
        form = SQLFORM(db.student_grade, record)
    return dict(form=form)
