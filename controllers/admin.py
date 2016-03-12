# -*- coding: utf-8 -*-

import collections
from cStringIO import StringIO
import csv
from datetime import datetime
from operator import itemgetter
import os

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.widgets.grids import ShadedRect
from reportlab.graphics.shapes import Drawing


def index():
    if auth.has_membership(1, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))

    return dict()


def classes_create():
    if auth.has_membership(1, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))

    # begin handle upload csv
    upload_folder = os.path.join(request.folder, 'uploads')

    formcsv = SQLFORM.factory(
        Field('file', 'upload', uploadfolder=upload_folder),
        submit_button='Upload')

    if formcsv.process(formname='class_upload').accepted and formcsv.vars.file:
        upload_file = os.path.join(upload_folder, formcsv.vars.file)
        records_loaded = 0

        with open(upload_file, 'rb') as csvfile:
            importreader = csv.reader(csvfile)
            importreader.next()  # Skip header row.

            for row in importreader:
                content_area = db(db.contentarea.name==row[4]).select().first()
                db.classes.insert(
                    name=row[0],
                    grade_level=int(row[1]),
                    start_date=datetime.strptime(row[2], '%m-%d-%Y'),
                    end_date=datetime.strptime(row[3], '%m-%d-%Y'),
                    content_area=content_area)

            records_loaded = importreader.line_num - 1

        response.flash = 'Loaded %d records' % (records_loaded,)

        os.remove(upload_file)
    # end handle upload csv

    # begin handle single insert
    form = SQLFORM.factory(db.classes, submit_button='Add Class')
    if form.process(formname='class_insert').accepted:
        db.classes.insert(
            name=form.vars.name,
            grade_level=form.vars.grade_level,
            start_date=datetime.strptime(form.vars.start_date, '%B %d, %Y'),
            end_date=datetime.strptime(form.vars.end_date, '%B %d, %Y'),
            content_area=form.vars.content_area)
    # end handle single insert

    return dict(form=form, formcsv=formcsv)


def teacher_create():
    if auth.has_membership(1, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))

    # begin handle upload csv
    upload_folder = os.path.join(request.folder, 'uploads')

    formcsv = SQLFORM.factory(
        Field('file', 'upload', uploadfolder=upload_folder),
        submit_button='Upload')

    if formcsv.process(formname='teacher_upload').accepted and formcsv.vars.file:
        upload_file = os.path.join(upload_folder, formcsv.vars.file)
        records_loaded = 0

        with open(upload_file, 'rb') as csvfile:
            importreader = csv.reader(csvfile)
            importreader.next()  # Skip header row.

            for row in importreader:
                uid = db.auth_user.insert(
                    first_name=row[0],
                    last_name=row[1],
                    email=row[2],
                    username=row[3],
                    password=CRYPT()(row[4])[0])

                auth.add_membership(user_id=uid,
                                    group_id=auth.id_group('Teacher'))

            records_loaded = importreader.line_num - 1

        response.flash = 'Loaded %d records' % (records_loaded,)

        os.remove(upload_file)
    # end handle upload csv

    # begin handle single insert
    form = SQLFORM.factory(db.auth_user, submit_button='Add Teacher')

    if form.process(formname='teacher_insert').accepted:
        uid = db.auth_user.insert(first_name=form.vars.first_name,
                                  last_name=form.vars.last_name,
                                  email=form.vars.email,
                                  username=form.vars.username,
                                  password=form.vars.password)

        auth.add_membership(user_id=uid,
                            group_id=auth.id_group('Teacher'))
    # end handle single insert

    return dict(form=form, formcsv=formcsv)


def student_create():
    if auth.has_membership(1, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))

    # begin handle upload csv
    upload_folder = os.path.join(request.folder, 'uploads')

    formcsv = SQLFORM.factory(
        Field('file', 'upload', uploadfolder=upload_folder),
        submit_button='Upload')

    if formcsv.process(formname='student_upload').accepted and formcsv.vars.file:
        upload_file = os.path.join(upload_folder, formcsv.vars.file)
        records_loaded = 0

        with open(upload_file, 'rb') as csvfile:
            importreader = csv.reader(csvfile)
            importreader.next()  # Skip header row.

            for row in importreader:
                uid = db.auth_user.insert(
                    first_name=row[0],
                    last_name=row[1],
                    email=row[2],
                    username=row[3],
                    password=CRYPT()(row[4])[0])

                db.student.insert(user_id=uid,
                                  school_id_number=row[5],
                                  grade_level=row[6],
                                  home_address=row[7],
                                  parent_email=row[8])

                auth.add_membership(user_id=uid,
                                    group_id=auth.id_group('Student'))

            records_loaded = importreader.line_num - 1

        response.flash = 'Loaded %d records' % (records_loaded,)

        os.remove(upload_file)
    # end handle upload csv

    # begin handle single insert
    form = SQLFORM.factory(db.auth_user, db.student,
                           submit_button='Add Student')

    if form.process(formname='student_insert').accepted:
        uid = db.auth_user.insert(first_name=form.vars.first_name,
                                  last_name=form.vars.last_name,
                                  email=form.vars.email,
                                  username=form.vars.username,
                                  password=form.vars.password)

        db.student.insert(user_id=uid,
                          school_id_number=form.vars.school_id_number,
                          grade_level=form.vars.grade_level,
                          home_address=form.vars.home_address,
                          parent_email=form.vars.parent_email)

        auth.add_membership(user_id=uid,
                            group_id=auth.id_group('Student'))
    # end handle upload csv

    return dict(form=form, formcsv=formcsv)


def parent_create():
    if auth.has_membership(1, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))

    # begin handle upload csv
    upload_folder = os.path.join(request.folder, 'uploads')

    formcsv = SQLFORM.factory(
        Field('file', 'upload', uploadfolder=upload_folder),
        submit_button='Upload')

    if formcsv.process(formname='parent_upload').accepted and formcsv.vars.file:
        upload_file = os.path.join(upload_folder, formcsv.vars.file)
        records_loaded = 0

        with open(upload_file, 'rb') as csvfile:
            importreader = csv.reader(csvfile)
            importreader.next()  # Skip header row.

            for row in importreader:
                uid = db.auth_user.insert(
                    first_name=row[0],
                    last_name=row[1],
                    email=row[2],
                    username=row[3],
                    password=CRYPT()(row[4])[0])

                auth.add_membership(user_id=uid,
                                    group_id=auth.id_group('Parent'))

            records_loaded = importreader.line_num - 1

        response.flash = 'Loaded %d records' % (records_loaded,)

        os.remove(upload_file)
    # end handle upload csv

    # begin handle single insert
    form = SQLFORM.factory(db.auth_user, submit_button='Add Parent')

    if form.process(formname='parent_insert').accepted:
        uid = db.auth_user.insert(first_name=form.vars.first_name,
                                  last_name=form.vars.last_name,
                                  email=form.vars.email,
                                  username=form.vars.username,
                                  password=form.vars.password)

        auth.add_membership(user_id=uid,
                            group_id=auth.id_group('Parent'))
    # end handle upload csv

    return dict(form=form, formcsv=formcsv)


def assign_teacher_to_class():
    if auth.has_membership(1, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))

    teacher_query = ((db.auth_group.id == 2)&
            (db.auth_membership.group_id == db.auth_group.id)&
            (db.auth_membership.user_id == db.auth_user.id))
    teacher_field = Field("Teacher",  requires=IS_IN_DB(db(teacher_query), "auth_user.id", '%(first_name)s'+' ' + '%(last_name)s', zero = None))

    class_query = ((db.classes.id > 0))
    class_field = Field("Class",  requires=IS_IN_DB(db(class_query), "classes.id", '%(name)s', zero = None))

    form = SQLFORM.factory(teacher_field, class_field, submit_button='Assign To Class')

    if form.process().accepted:
        row = db.gradebook(teacher = form.vars.Teacher, classes = form.vars.Class)
        if not row:
            db.gradebook.insert(teacher = form.vars.Teacher, classes = form.vars.Class)
        else:
            response.flash = "Already Exist"
            pass


    return dict(form=form)


def assign_student_to_class():
    if auth.has_membership(1, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))

    student_query = ((db.student.id > 0)&
                    (db.student.user_id == db.auth_user.id))
    students = db(student_query).select(db.student.id,
                                        db.student.school_id_number,
                                        db.auth_user.first_name,
                                        db.auth_user.last_name)

    options = []
    for row in students:
        text = '%s %s  -  %s' % (row.auth_user.first_name,
                                 row.auth_user.last_name,
                                 row.student.school_id_number)
        options.append(OPTION(text, _value=row.student.id))

    name_id = SELECT(options,
                     _id='students',
                     _name='students',
                     _class='generic-widget form-control')

    class_query = ((db.classes.id > 0))
    class_field = Field("Class",
                        requires=IS_IN_DB(db(class_query),
                                          "classes.id",
                                          '%(name)s',
                                          zero = None))

    form = SQLFORM.factory(class_field, submit_button='Assign To Class')
    form.insert(-1, name_id)


    if form.process().accepted:
        row = db.student_classes(student_id=form.vars.students,
                                 class_id=form.vars.Class)
        if not row:
            db.student_classes.insert(student_id=form.vars.students,
                                      class_id=form.vars.Class)
        else:
            response.flash = "Student already in that class!"
            pass

    return dict(form=form, name_id=name_id)



def assign_parent_to_student():
    if auth.has_membership(1, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))

    parent_query = ((db.auth_group.id == 4)&
            (db.auth_membership.group_id == db.auth_group.id)&
            (db.auth_membership.user_id == db.auth_user.id))
    parent_field = Field("Parent",  requires=IS_IN_DB(db(parent_query), "auth_user.id", '%(first_name)s'+' ' + '%(last_name)s', zero = None))

    student_query = ((db.student.id > 0)&
                    (db.student.user_id == db.auth_user.id))
    students = db(student_query).select(db.student.id, db.student.school_id_number, db.auth_user.first_name, db.auth_user.last_name)

    options = []
    for row in students:
        text = '%s %s  -  %s' % (row.auth_user.first_name, row.auth_user.last_name, row.student.school_id_number)
        options.append(OPTION(text, _value=row.student.id))

    name_id = SELECT(options, _name='students',
                            _class='generic-widget form-control')

    form = SQLFORM.factory(parent_field, submit_button='Assign To Student')
    form.insert(-1, name_id)


    if form.process().accepted:
        row = db.parent_student(parent_id = form.vars.Parent, student_id = form.vars.students)
        if not row:
            db.parent_student.insert(parent_id = form.vars.Parent , student_id = form.vars.students)
        else:
            response.flash = "Already Exist"
            pass

    return dict(form=form, name_id=name_id)


@auth.requires(auth.has_membership('Administrator', auth.user_id),
               requires_login=True)
def standard_import():

    # begin handle upload csv
    upload_folder = os.path.join(request.folder, 'uploads')

    formcsv = SQLFORM.factory(
        Field('file', 'upload', uploadfolder=upload_folder),
        submit_button='Upload')

    if formcsv.process(formname='standard_upload').accepted and formcsv.vars.file:
        upload_file = os.path.join(upload_folder, formcsv.vars.file)
        records_loaded = 0

        with open(upload_file, 'rb') as csvfile:
            importreader = csv.reader(csvfile)
            importreader.next()  # Skip header row.

            for row in importreader:
                content_area = db(db.contentarea.name==row[3]).select().first()
                db.standard.insert(
                    reference_number=row[0],
                    short_name=row[1],
                    description=row[2],
                    content_area=content_area,
                    grade_level=int(row[4]))

            records_loaded = importreader.line_num - 1

        response.flash = 'Loaded %d records' % (records_loaded,)

        os.remove(upload_file)
    # end handle upload csv

    # begin handle single insert
    form = SQLFORM.factory(db.standard, submit_button='Add Standard')
    if form.process(formname='standard_insert').accepted:
        db.standard.insert(
            reference_number=form.vars.reference_number,
            short_name=form.vars.short_name,
            description=form.vars.description,
            content_area=form.vars.content_area,
            grade_level=form.vars.grade_level)
    # end handle single insert

    return dict(form=form, formcsv=formcsv)
    

def standard_overview():
    if auth.has_membership(1, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))

    grade_query = ((db.classes.grade_level))
    grade = db(grade_query).select(db.classes.grade_level)

    grade_list = []

    for row in grade:
        grade_list.append(row.grade_level)

    grade_list = list(set(grade_list))

    content_ids={}
    content_names={}
    overview_data = {}
    content_area_all = {}

    for grade in grade_list:
        standard_query = ((db.classes.grade_level == grade) &
                          (db.classes.id == db.student_classes.class_id) &
                          (db.student.id == db.student_classes.student_id) &
                          (db.student.id == db.student_grade.student_id) &
                          (db.grade.id == db.student_grade.grade_id) &
                          (db.grade.id == db.grade_standard.grade_id) &
                          (db.standard.id == db.grade_standard.standard_id) &
                          (db.classes.id == db.class_grade.class_id) &
                          (db.grade.id == db.class_grade.grade_id) &
                          (db.standard.content_area == db.contentarea.id))

        standard_list = db(standard_query).select(
            db.standard.id,
            db.standard.short_name,
            db.standard.reference_number,
            db.student_grade.student_score,
            db.grade.score,
            db.contentarea.id,
            db.contentarea.name)

        content_area = {}
        standard_dict = {}

        for row in standard_list:
            if row.standard.id in standard_dict.keys():
                if((row.grade.score != 0.0) | (row.student_grade.student_score != 0.0)):
                    max_score = standard_dict[row.standard.id][0] + row.grade.score
                    student_score = standard_dict[row.standard.id][1] + row.student_grade.student_score
                    standard_dict[row.standard.id] = [max_score,
                                                      student_score,
                                                      row.standard.reference_number,
                                                      row.standard.short_name]
            else:
                content_area[row.contentarea.id]= row.contentarea.name
                standard_dict[row.standard.id] = [row.grade.score,
                                                  row.student_grade.student_score,
                                                  row.standard.reference_number,
                                                  row.standard.short_name]

        content_area_all[grade] = content_area
        overview_data[grade] = standard_dict

    #need content Name and contentID list
    return dict(overview_data=overview_data, content_area_all=content_area_all)


def class_list():
    if auth.has_membership(1, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))

    class_query = ((db.classes.id > 0)&
             (db.classes.content_area == db.contentarea.id))
    class_query_list = db(class_query).select(db.classes.grade_level, db.contentarea.name,  db.classes.name, db.classes.id)

    class_list_data = {}
    for row in class_query_list:

        teacher_query = ((db.classes.id == row.classes.id)&
                         (db.gradebook.classes == db.classes.id)&
                         (db.gradebook.teacher == db.auth_user.id))
        teacher = db(teacher_query).select(db.auth_user.first_name, db.auth_user.last_name)
        if len(teacher) > 0:
            class_list_data[row.classes.id] = [ row.classes.grade_level, row.contentarea.name, row.classes.name, teacher[0].first_name + " " +  teacher[0].last_name ]
        else:
            class_list_data[row.classes.id] = [ row.classes.grade_level, row.contentarea.name, row.classes.name, "N/A" ]

    return dict(class_list_data = class_list_data)


def teacher_list():
    if auth.has_membership(1, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))

    query = ((db.auth_membership.group_id == 2)&
             (db.auth_user.id == db.auth_membership.user_id))

    teacher_list = db(query).select(db.auth_user.first_name, db.auth_user.last_name, db.auth_user.username, db.auth_user.email)

    return dict(teacher_list = teacher_list)


def student_list():
    if auth.has_membership(1, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))

    query = ((db.auth_group.id == 3)&
             (db.auth_group.id == db.auth_membership.group_id)&
             (db.auth_user.id == db.auth_membership.user_id)&
             (db.auth_user.id == db.student.user_id))

    student_list = db(query).select(db.auth_user.first_name, db.auth_user.last_name, db.student.school_id_number, db.auth_user.username, db.auth_user.email)

    return dict(student_list = student_list)


def parent_list():
    if auth.has_membership(1, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))

    query = ((db.auth_membership.group_id == 4)&
             (db.auth_user.id == db.auth_membership.user_id))

    parent_list = db(query).select(db.auth_user.first_name, db.auth_user.last_name, db.auth_user.username, db.auth_user.email)

    return dict(parent_list = parent_list)


def teacher_class():
    if auth.has_membership(1, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))

    query = ((db.auth_user.id == db.gradebook.teacher)&
             (db.gradebook.classes == db.classes.id)&
             (db.classes.content_area == db.contentarea.id))
    teacher_class = db(query).select(db.classes.grade_level, db.classes.name, db.auth_user.first_name, db.auth_user.last_name, db.auth_user.id)

    view_data = {}
    for row in teacher_class:
        if row.auth_user.id in view_data.keys():
            view_data[row.auth_user.id][3].append(row.classes.name)
        else:
            view_data[row.auth_user.id] = [row.auth_user.first_name, row.auth_user.last_name, row.classes.grade_level, [row.classes.name]]


    return dict(view_data = view_data)


def student_class():
    if auth.has_membership(1, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))

    query = ((db.student_classes.id > 0)&
             (db.student_classes.student_id == db.student.id)&
             (db.student.user_id == db.auth_user.id)&
             (db.student_classes.class_id == db.classes.id))
    student_class =  db(query).select(db.auth_user.first_name, db.auth_user.last_name, db.student.school_id_number, db.auth_user.username, db.auth_user.email, db.classes.name)

    view_data = {}
    for row in student_class:
        if row.student.school_id_number in view_data.keys():
            view_data[row.student.school_id_number][4].append(row.classes.name)
        else:
            view_data[row.student.school_id_number] = [row.auth_user.first_name, row.auth_user.last_name, row.student.school_id_number, row.auth_user.username, [row.classes.name]]

    sorted_view_data = collections.OrderedDict(sorted(view_data.items()))
    view_data = sorted_view_data

    return dict(view_data = view_data)


def parent_student():
    if auth.has_membership(1, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))

    query = ((db.parent_student.id > 0)&
             (db.parent_student.parent_id == db.auth_user.id))
    parent_query = db(query).select(db.auth_user.ALL, db.parent_student.ALL)
    parent_dict = {}
    for row in parent_query:
        if row.auth_user.id in parent_dict.keys():
            parent_dict[row.auth_user.id][3].append(row.parent_student.student_id)
        else:
            parent_dict[row.auth_user.id] = [row.auth_user.id, row.auth_user.first_name, row.auth_user.last_name, [row.parent_student.student_id] ]

    view_data = {}
    for key in parent_dict.keys():
        view_data[key] = [parent_dict[key], []]

        for student in parent_dict[key][3]:
            student_query = ((db.student.id == student)&
                     (db.student.user_id == db.auth_user.id))
            student_info = db(student_query).select(db.auth_user.ALL)
            for student in student_info:
                view_data[key][1].append(student.first_name + " " + student.last_name)

    return dict(view_data = view_data)


def detail():
    grade_level = (request.args(0) != None) and request.args(0, cast=int) or None
    content_id = (request.args(1) != None) and request.args(1, cast=int) or None

    content_name = db(db.contentarea.id == content_id).select(db.contentarea.name)

    standard_query = ((db.classes.grade_level == grade_level)&
                      (db.classes.id == db.student_classes.class_id)&
                      (db.student.id == db.student_classes.student_id)&
                      (db.student.id == db.student_grade.student_id)&
                      (db.grade.id == db.student_grade.grade_id)&
                      (db.grade.id == db.grade_standard.grade_id)&
                      (db.standard.id == db.grade_standard.standard_id)&
                      (db.classes.id == db.class_grade.class_id)&
                      (db.grade.id == db.class_grade.grade_id)&
                      (db.standard.content_area == db.contentarea.id)&
                      (db.contentarea.id == content_id))

    standard_list = db(standard_query).select(db.standard.id, db.standard.short_name, db.standard.reference_number,db.student_grade.student_score, db.grade.score)

    standard_dict = {}
    for row in standard_list:
        if row.standard.id in standard_dict.keys():
            if((row.grade.score != 0.0) | (row.student_grade.student_score != 0.0)):
                max_score = standard_dict[row.standard.id][0] + row.grade.score
                student_score = standard_dict[row.standard.id][1] + row.student_grade.student_score
                standard_dict[row.standard.id] = [max_score, student_score, row.standard.reference_number, row.standard.short_name]
        else:
            standard_dict[row.standard.id] = [row.grade.score, row.student_grade.student_score, row.standard.reference_number, row.standard.short_name]

    detail_data = {}
    for key in standard_dict.keys():
        detail_data[key] = [standard_dict[key][2], standard_dict[key][3], round(standard_dict[key][1]/standard_dict[key][0]*100,2)]

    sorted_detail_data = collections.OrderedDict(sorted(detail_data.items()))
    detail_data = sorted_detail_data

    return dict(content_name=content_name, grade_level=grade_level, content_id=content_id, detail_data=detail_data )


def pdf_overview():

    #get arguments passed from previous page
    grade = (request.args(0) != None) and request.args(0, cast=int) or None
    content_area_id = (request.args(1) != None) and request.args(1, cast=int) or None

    #get a pdf from the helper function
    pdf = create_single_grade_pdf(grade,content_area_id)
    return pdf


def create_single_grade_pdf(grade,content_area_id):
    '''--Variables--'''
    school_level = []
    Story=[]
    Elements=[]
    contentarea_name = ""
    buff = StringIO()
    formatted_time = time.ctime()
    minimum = 100
    standard_averages=[[]]
    standard_table=[]
    
    content_areas = []
    
    '''------'''
    styles = getSampleStyleSheet()
    HeaderStyle = styles["Heading1"]

    #get the Content Area Name
    query = ((content_area_id == db.contentarea.id))
    results = db(query).select(db.contentarea.name)
    for row in results:
        contentarea_name = row.name


    #Create the name for the PDf being returned
    pdfName = "Grade_"+str(grade)+"_"+contentarea_name+"_SR"+".pdf"

    #set up the response headers so the browser knows to return a PDF document
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] ='attachment;filename=%s;'%pdfName
    doc = SimpleDocTemplate(buff,pagesize=letter,rightMargin=72,leftMargin=72,topMargin=72,bottomMargin=18)
    doc.title=pdfName

    #Set up some styles
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='Indent', rightIndent=3))
    styles.add(ParagraphStyle(name = 'Title2',
                                  parent = styles['Normal'],
                                  fontName = 'DejaVuSansCondensed',
                                  fontSize = 18,
                                  leading = 22,
                                  spaceAfter = 6),
                                  alias = 'title2')


    #Time-Stamp
    ptext = '<font size=12>%s</font>' % formatted_time
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    Elements.extend(ptext)

    #Administrator
    ptext='<font size=12><b>Administrator</b></font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))
    Elements.extend(ptext)

    #Grade Number and Content Area
    ptext = '<font size=12><b>Grade %s %s Standards Report</b></font>'%(grade, contentarea_name)
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 7))
    Elements.extend(ptext)
    Story.append(Spacer(1,40))

    #Graph Title
    ptext = '<font size=15><b>Standards Progress</b></font>'
    Story.append(Paragraph(ptext, styles["title"]))


    i = 0
    #get all the standards for a specific grade and content area
    standard_query = standard_query = ((db.classes.grade_level == grade)&
                      (db.classes.id == db.student_classes.class_id)&
                      (db.student.id == db.student_classes.student_id)&
                      (db.student.id == db.student_grade.student_id)&
                      (db.grade.id == db.student_grade.grade_id)&
                      (db.grade.id == db.grade_standard.grade_id)&
                      (db.standard.id == db.grade_standard.standard_id)&
                      (db.classes.id == db.class_grade.class_id)&
                      (db.grade.id == db.class_grade.grade_id)&
                      (db.standard.content_area == db.contentarea.id)&
                      (db.contentarea.id == content_area_id))

    standard_list = db(standard_query).select(db.standard.id, db.standard.short_name, db.standard.reference_number,db.student_grade.student_score, db.grade.score, db.contentarea.name)
    standard_ref_list=[]
    #Setup the Dictionary of standard averages
    standard_dict = {}
    for row in standard_list:
        if row.standard.id in standard_dict.keys():
            if((row.grade.score != 0.0) | (row.student_grade.student_score != 0.0)):
                max_score = standard_dict[row.standard.id][0] + row.grade.score
                student_score = standard_dict[row.standard.id][1] + row.student_grade.student_score
                standard_dict[row.standard.id] = [max_score, student_score, row.standard.reference_number, row.standard.short_name]
        else:
            standard_dict[row.standard.id] = [row.grade.score, row.student_grade.student_score, row.standard.reference_number, row.standard.short_name]

    standard_table = []
    standard_averages=[[]]

    #set up the 2D list of Standard Averages
    for standard in sorted(standard_dict.keys()):
        standard_ref_list.append(standard_dict[standard][2])
        standard_table.append([])
        current_avg = (standard_dict[standard][1]/standard_dict[standard][0])*100
        if minimum > current_avg:
            minimum = current_avg
        standard_table[i].append(standard_dict[standard][3]+": "+format((standard_dict[standard][1]/standard_dict[standard][0])*100,'.2f')+"%")
        standard_averages[0].append(int(round((standard_dict[standard][1]/standard_dict[standard][0])*100)))
        i+=1
    sorted(standard_table,key=lambda l:l[0])

    '''---Graph---'''
    drawing = Drawing(600, 200)
    data = standard_averages
    bc = VerticalBarChart()

    #location in the document (x,y)
    bc.x = 10
    bc.y = 30

    #width and height of the graph
    bc.height = 225
    bc.width = 400
    bc.data = data
    bc.categoryAxis.drawGridLast=True
    bc.categoryAxis.gridStart=0
    bc.categoryAxis.gridStrokeLineCap = 2
    bc.categoryAxis.gridEnd=3
    #bc.barLabels = 

    #Update colors of the bars in the graph
    bc.bars.symbol = ShadedRect()
    bc.bars.symbol.fillColorStart = colors.lightblue
    bc.bars.symbol.fillColorEnd = colors.lightblue
    bc.bars.symbol.strokeWidth = 0


    #this draws a line at the top of the graph to close it. 
    bc.strokeColor = colors.black

    #Y-axis min, max, and steps.
    if minimum != 100:
        bc.valueAxis.valueMin = minimum -10
    else:
        bc.valueAxis.valueMin = 50
    bc.valueAxis.valueMax = 100
    bc.valueAxis.valueStep = 5

    #where to anchor the origin of the graph
    bc.categoryAxis.labels.boxAnchor = 'ne'

    #Locations of labels for the X-axis
    bc.categoryAxis.labels.dx = 2
    bc.categoryAxis.labels.dy = -2

    bc.barLabels.nudge = -10
    bc.barLabelFormat = '%0.2f%%'
    bc.barLabels.dx = 0
    bc.barLabels.dy = 0
    #The angle of the lables for the X-axis
    bc.categoryAxis.labels.angle = 30
    #List of the categories to place on the X-axis
    bc.categoryAxis.categoryNames = standard_ref_list
    drawing.add(bc)
    '''------'''
    '''--Graph Legend--'''
    #Graph Legend
    legend = Legend()
    legend.alignment = 'right'
    legend.x = 420
    legend.y = 150
    legend.deltax = 60
    legend.dxTextSpace = 10
    legend.columnMaximum = 4

    legend.colorNamePairs = [(colors.lightblue, 'grade average')]
    drawing.add(legend, 'legend')
    drawing_title = "Bar Graph"
    Story.append(drawing)

    #build PDF document and return it
    doc.build(Story)
    pdf = buff.getvalue()
    buff.close()
    return pdf



def settings():
    if auth.has_membership(1, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))

    location_Field = Field("location", default="trend", writable=False)
    form = SQLFORM.factory(location_Field, db.settings.setting, submit_button='Save Setting')
    if form.accepts(request,session):
        num = float(request.vars.setting)
        db.settings.update_or_insert(db.settings.location=="trend", location = "trend", setting = num)
        response.flash = 'New Threshold Set'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'Please Enter Setting'

    trend_num_query = db(db.settings.location == "trend").select(db.settings.setting)
    trend_num = trend_num_query[0].setting
    return dict(form=form, trend_num=trend_num)
