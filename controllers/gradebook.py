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
def create():
    """generate form for new gradebook entry, redirect to index"""
    form = SQLFORM(db.gradebook).process(next=URL('index'))
    return dict(form=form)


def overview():
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
###########
       # create_single_class_pdf(teacher_name, class_id, class_name, average, total_students, total_grades, table_grid)
        
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

        
        
        
        '''
    #To display standards
        query = ((db.classes.id==class_id) &
                     (db.class_grade.class_id==class_id) &
                     (db.class_grade.grade_id==db.grade.id) &
                     (db.student_grade.grade_id==db.grade.id) &
                     (db.grade.id==db.grade_standard.grade_id) &
                     (db.standard.id==db.grade_standard.standard_id) &
                     (db.standard.content_area == db.contentarea.id))

        standard_list = db(query).select(db.standard.id, db.standard.short_name, db.standard.reference_number,db.student_grade.student_score, db.grade.score)

        standard_dict = {}
        for row in standard_list:
            if row.standard.id in standard_dict.keys():
                if((row.grade.score != 0.0) | (row.student_grade.student_score != 0.0)):
                    max_score = standard_dict[row.standard.id][0] + row.grade.score
                    student_score = standard_dict[row.standard.id][1] + row.student_grade.student_score
                    standard_dict[row.standard.id] = [max_score, student_score, row.standard.reference_number, row.standard.short_name]

            else:
                standard_dict[row.standard.id] = [row.grade.score, row.student_grade.student_score, row.standard.reference_number, row.standard.short_name]
                standard_grid = get_student_assignments(teacher_id,class_id,row.standard.id)'''
        create_single_class_pdf(teacher_name, class_id, class_name, average, total_students, total_grades, standard_table)

    #build_table_pdf()
    #create_a_test_pdf(class_names, class_averages_dict, classes_dict, standards_dict)
    #create_single_class_pdf(class_id, class_name, class_average, standard_dict)
    return dict(class_names=class_names,
                class_averages_dict=class_averages_dict)


    
def create_single_class_pdf(teacher_name, class_id,class_name, class_average, total_students, total_grades, table_grid):
    doc = SimpleDocTemplate("single_class.pdf",pagesize=letter,rightMargin=72,leftMargin=72,topMargin=72,bottomMargin=18)
    Story=[]
    formatted_time = time.ctime()
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='Indent', rightIndent=3))
    ptext = '<font size=12>%s</font>' % formatted_time

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))

    #Teacher Name
    ptext='<font size=12><b>%s %s</b></font>'%(teacher_name.first_name, teacher_name.last_name)
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))

    #Class Name
    ptext = '<font size=12>%s: </font>'%(class_name)
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 7))

    #Class Average
    ptext = '<font size=12>Class Average:%s%%</font>'%(class_average)
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1,12))
    
    #Total Students
    ptext = '<font size=12>Total Students:%s</font>'%(total_students)
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1,12))
    
    #Total Assignments
    ptext = '<font size=12>Total Assignments:%s</font>'%(total_grades)
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1,12))
    Story.append(Spacer(1,40))

    #Standards Data goes here:
    ptext = '<font size=18>--STANDARD DATA GOES HERE--</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1,40))

    #Standards Table
    t=Table(table_grid)
    t.setStyle(t.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                      ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),])))
    Story.append(t)



    doc.build(Story)
def build_table_pdf(): 
    doc = SimpleDocTemplate("complex_cell_values.pdf", pagesize=letter)
    # container for the 'Flowable' objects
    elements = []
 
    styleSheet = getSampleStyleSheet()

    P0 = Paragraph('''
               <b>A pa<font color=red>r</font>a<i>graph</i></b>
               <super><font color=yellow>1</font></super>''',
               styleSheet["BodyText"])
    P = Paragraph('''
    <para align=center spaceb=3>The <b>ReportLab Left
    <font color=red>Logo</font></b>
    Image</para>''',
    styleSheet["BodyText"])
    data= [['A', 'B', 'C', P0, 'D'],
       ['00', '01', '02', '04'],
       ['10', '11', '12', '14'],
       ['20', '21', '22', '23', '24'],
       ['30', '31', '32', '33', '34']]
 
    t=Table(data,style=['Normal'])
    t._argW[3]=1.5*inch
 
    elements.append(t)
    # write the document to disk
    doc.build(elements)
