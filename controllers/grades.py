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
    if not class_id:
        response.flash = T("Class ID Required.")
        session.flash = T("Class ID Required.")

    teacher_id = auth.user_id
    exist = db.classes(class_id)
    content_id = 1

    if not exist:
        response.flash = T("Class does not exist.")
        session.flash = T("Class does not exist.")

    query = ((db.classes.id==class_id) &
             (db.classes.content_area==db.contentarea.id) &
             (db.standard.content_area==db.contentarea.id))

    # # Creating the drob down menu for Standard
    standards = db(query).select(db.standard.id,
                                 db.standard.short_name,
                                 db.standard.reference_number)

    options = []
    for row in standards:
        text = '%s - %s' % (row.reference_number,
                            row.short_name)
        options.append(OPTION(text, _value=row.id))

    standards_menu = SELECT(options, _name='standards', _multiple='multiple',
                            _class='generic-widget form-control')

    form = SQLFORM(db.grade)
    form.insert(-1, standards_menu)

    # Processing the form
    if form.validate():
        response.flash = 'New grade created.'

    #     # inserting the new grade into db.grade
    #     id = db.grade.insert(**db.grade._filter_fields(form.vars))

    #     # creating the link between class and grade.
    #     db.class_grade.insert(class_id = class_id,grade_id = id)

    #     # creating the link between grade and standard
    #     if form.vars.standard != zero:
    #         db.grade_standard.insert(grade_id = id, standard_id = form.vars.standard)

    #     # get student_class query (get_class_roster(tearcher_id, class_id))
    #     # for-loop through students
    #     # add to the student_grade table with (student_id,grade_id, 0)
    #     for student in get_class_roster(teacher_id, class_id):
    #         db.student_grade.insert(student_id=student[0], grade_id = id, student_score = 0)

    #     response.flash = T("New assignment successfully created")
    #     session.flash = T("New assignment successfully created")
    #     redirect(URL("classes","index/"+class_id))

    # #Form error handling.
    # elif form.errors:
    #     response.flash = T("Form Has Errors")
    #     session.flash = T("Form Has Errors")

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
