# -*- coding: utf-8 -*-
# try something like
import datetime

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
        class_id = request.args(0)
        teacher_id = request.args(1)
        content_id = 1
        exist = db.classes(class_id)

        #If class does not exist, redirects.
        if (exist == None):
            response.flash = T("Class Does Not Exist")
            session.flash = T("Class does not exist.")

            #Redirect to previous link if via link, else redirec to main page.
        #    if (request.env.http_referer==None):
        #        redirect(URL("default","index"))
          #  else:
         #       redirect(request.env.http_referer)

    #If no argument given, throws Invalid class and redirect.
    except:
        response.flash = T("Invalid Class")
        session.flash = T("Invalid Class")

            #If class does not exist, redirects.
    #if (request.env.http_referer==None):
       # redirect(URL("default","index"))

        #Redirect to previous link if via link, else redirec to main page.
    #else:
     #   redirect(request.env.http_referer)

    query = ((db.classes.id==class_id) &
        (db.classes.id==db.student_classes.class_id) &
        (db.student_classes.student_id==db.student.id) &
        (db.student.user_id==db.auth_user.id) &
        (db.student.id==db.student_grade.student_id) &
        (db.student_grade.grade_id==db.grade.id) &
        (db.grade.id==db.grade_standard.grade_id) &
        (db.standard.id==db.grade_standard.standard_id) &
        (db.standard.content_area == db.contentarea.id))
    
    query = ((class_id == db.classes.id)&
            (db.standard.content_area == db.classes.content_area))
    
    
    
            #((class_id == db.classes.id) & 
            # (db.classes.id == db.class_grade.class_id) &
             #(db.grade.id == db.class_grade.grade_id) &
             #(db.grade.id == db.grade_standard.grade_id) &
             #(db.grade_standard.standard_id == db.standard.id) &
             #(db.classes.content_area == db.standard.content_area))

#    standard_list = db(query).select(db.standard.id, db.standard.short_name, db.standard.reference_number,db.student_grade.student_score,  db.grade.score)
    #Creating the drob down menu for Standard
    standardR = Field('standard', requires=IS_IN_DB(db(query), 'standard.id', '%(reference_number)s'+': '+'%(short_name)s',zero=T('Standard')))
    #query = ((db.classes.id == class_id) & (db.classes.content_area==db.standard.content_area))
    now = datetime.datetime.utcnow()
    now = now - datetime.timedelta(minutes=now.minute % 10,
                             seconds=now.second,
                             microseconds=now.microsecond)

    form = SQLFORM.factory(db.grade,standardR)

    form.vars.display_date = now
    form.vars.date_assigned = now
    form.vars.due_date = now + datetime.timedelta(days=1)

    #Processing the form
    if form.process().accepted:

        #inserting the new grade into db.grade
        id = db.grade.insert(**db.grade._filter_fields(form.vars))

        #creating the link between class and grade.
        db.class_grade.insert(class_id = class_id,grade_id = id)
        #creating the link between grade and standard
        db.grade_standard.insert(grade_id = id, standard_id = form.vars.standard)

        #get student_class query (get_class_roster(tearcher_id, class_id))
        #for-loop through students
        #add to the student_grade table with (student_id,grade_id, 0)
        for student in get_class_roster(teacher_id, class_id):
            db.student_grade.insert(student_id=student[0], grade_id = id, student_score = 0)

        response.flash = T("New assignment sucssfully created")
        session.flash = T("New assignment sucssfully created")
        redirect(URL("classes","index/"+class_id))
    #Form error handling.
    elif form.errors:
        response.flash = T("Form Has Errors")
        session.flash = T("Form Has Errors")
    #else:
       # response.flash = T("Please Fill Out The Form")
        #session.flash = T("Please Fill Out The Form")
    return dict(form=form)


def edit():
    try:
        record = request.vars[0]
        form = SQLFORM(db.student_grade, record)
    except:
        record = 0
        form = SQLFORM(db.student_grade, record)
    return dict(form=form)
