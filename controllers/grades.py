# -*- coding: utf-8 -*-
# try something like


def index():
    #constraints = db.gradebook.teacher == auth.user.id
    #grid = SQLFORM.smartgrid(db.grade)

    #grid = db(db.grade.name).select(join=db.grade.on((db.grade.name==db.student_grade.grade_id)))
    
    grid = db().select(db.grade.id, db.grade.name, db.grade.display_date,
                       db.grade.date_assigned, db.grade.due_date,
                       db.grade.grade_type,db.grade.score, db.grade.isPassFail)
    return dict(grid=grid)

def query():
    gname = request.vars['gname']
    assignment = db.student_grade.grade_id==gname
    c1 = (db.student.user_id== db.auth_user.id)& (db.student.id == db.student_grade.student_id)
    grade_query = db(assignment).select(db.auth_user.id, db.auth_user.first_name, db.auth_user.last_name, db.student_grade.student_score, left=db.student_grade.on(c1))
    return dict(grade_query=grade_query)


def create():
    '''Generating form for creating a new assignment'''
    #If there is an argument class id, check to see if db.classes contains that class.
    try:
        class_id = request.args[0]
        exist = db.classes(class_id)

        #If class does not exist, redirects.
        if (exist == None):
            response.flash = T("Class Does Not Exist")
            session.flash = T("Class does not exist.")

            #Redirect to previous link if via link, else redirec to main page.
            if (request.env.http_referer==None):
                redirect(URL("default","index"))
            else:
                redirect(request.env.http_referer)

    #If no argument given, throws Invalid class and redirect.
    except:
        response.flash = T("Invalid Class")
        session.flash = T("Invalid Class")

        #If class does not exist, redirects.
        if (request.env.http_referer==None):
            redirect(URL("default","index"))

        #Redirect to previous link if via link, else redirec to main page.
        else:
            redirect(request.env.http_referer)

    #Creating the drop down menu
    gradeT = Field('grade_type', requires=IS_IN_DB(db, 'grade_type.id', '%(name)s',zero=T('Choose Grade Type')))

    #Creating the form.
    form = SQLFORM.factory(db.grade.name,
                           db.grade.display_date,
                           db.grade.date_assigned,
                           db.grade.due_date, gradeT,
                           db.grade.score,
                           db.grade.isPassFail)

    #Processing the form
    if form.process().accepted:

        #inserting the new grade into db.grade
        id = db.grade.insert(**db.grade._filter_fields(form.vars))

        #creating the link between class and grade.
        db.class_grade.insert(class_id = class_id,grade_id = id)
        response.flash = T("New assignment sucssfully created")
        session.flash = T("New assignment sucssfully created")

    #Form error handling.
    elif form.errors:
        response.flash = T("Form Has Errors")
        session.flash = T("Form Has Errors")
    else:
        response.flash = T("Please Fill Out The Form")
        session.flash = T("Please Fill Out The Form")


def edit():
    try:
        record = request.vars[0]
        form = SQLFORM(db.student_grade, record)
    except:
        record = 0
        form = SQLFORM(db.student_grade, record)
    return dict(form=form)
