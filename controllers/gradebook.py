# -*- coding: utf-8 -*-
# requires authorized login to return classes

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
#from formula import CurrentPageColSum, PreviousPagesColSum, TotalPagesColSum,RowNumber
#from spreadsheettable import SpreadsheetTable
from cgi import escape
import time

@auth.requires_login()
def index():
    """pull up teacher and classes that match current user and return a grid with the result"""
    if auth.has_membership(2, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))

    # declare constraints as where thea teacher matches an authorized user id
    constraints = db.gradebook.teacher == auth.user.id
    grid = db(constraints).select(join=db.gradebook.on(
        (db.gradebook.teacher==db.auth_user.id) & (db.gradebook.classes==db.classes.id)))
    # response.flash = 'Class List - %(first_name)s' % auth.user

    #class_data contains many classes, each class = [name, id, content_area, average]
    class_data = []
    for row in grid:
        average = 0
        try:
            average = format(get_class_total_score(row.classes.id) /
                             get_class_total_possible(row.classes.id) * 100.00, '.2f')
        except:
            pass
        single_class=[row.classes.name, row.classes.id, row.classes.content_area.name, average]
        class_data.append(single_class)

    return dict(class_data=class_data)

# This should go under manage - assuming this is a school/district maanged tool,
# teachers won't add classes to their gradebooks.
@auth.requires_login()
def create():
    """generate form for new gradebook entry, redirect to index"""
    form = SQLFORM(db.gradebook).process(next=URL('index'))
    return dict(form=form)

@auth.requires_login()
def overview():
    '''THIS METHOD IS NOT DOING ANYTHING RIGHT NOW. CONSIDER DELETING?'''
    if auth.has_membership(2, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))
    teacher_id = auth.user_id
    query = teacher_classes_query(teacher_id)
    class_names = db(query).select(db.classes.name)
    class_ids = db(query).select(db.classes.id)

    teacher_name = get_teacher_name(teacher_id)
    standard_table=[[]]
    standard_dict ={}
    class_averages_dict={}
    table_grid = [['Math Standard 1', 'assignment1','assignment2'],
                  ['Math Standard 2', 'Test1'],
                 ['Math Standard 3', 'Assignment3', 'assignment4']]
    '''
    get_student_assignments(teacher_id, class_id, standard_id)
    '''
    for cid in class_ids:
        class_id = cid
        class_name = get_class_name(cid).name
        total_score = get_class_total_score(cid)
        total_possible= get_class_total_possible(cid)
        average = 0
        #To display number of students.
        total_students = len(get_class_roster(teacher_id, cid))
        #To display number of assignments
        grade_query = ((db.class_grade.class_id == cid) &
                       (db.class_grade.grade_id == db.grade.id))
        total_grades = db(grade_query).count()
        #get averages and set up the outer dictionary.
        average = round(total_score / total_possible * 100.0, 2)
        standards = get_standards_for_class(cid)
        total_score =0
        students_score = 0
        i=0
        for row in standards:
            #add standard.reference_number to beginning of inner list
            a_list=[]
            standard_table.append(a_list)
            standard_table[i].append(row.reference_number)
            #get all the grades for the associated class and current standard
            query = class_assignment_query(cid, row.id)
            grades = db(query).select(db.grade.id, db.grade.name, db.grade.score)
            for grade in grades:
                #update total_score
                grade_name = grade.name
                total_score = grade.score
                students_score = 0
                #get all student_grades attached to this grade
                query =((db.grade.id==grade.grade.id)&
                        (db.grade.id == db.student_grade.grade_id)&
                        (db.student_grade.student_id==db.student.id))
                scores = db(query).select(db.student.id, db.student_grade.student_score)
                j=0
                #add up all scores
                for score in scores:
                    students_score = students_score + score.student_score
                    j = j+1

                total_score = total_score *j
                assignment_average = (students_score/total_score)*100
                assignment = grade_name+": "+assignment_average
                standard_table[i].append(assignment)
            i = i+1

    return dict(class_names=class_names,
                class_averages_dict=class_averages_dict)
