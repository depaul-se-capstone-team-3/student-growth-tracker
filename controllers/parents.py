# -*- coding: utf-8 -*-
# try something like
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from operator import itemgetter
import collections
from cStringIO import StringIO
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.lineplots import GridLinePlot
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.legends import LineLegend
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics import renderPDF
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.widgets.grids import ShadedRect
from reportlab.graphics.shapes import Drawing


@auth.requires_login()
def index():
    if auth.has_membership(4, auth.user_id):
        class_id = (request.args(0) != None) and request.args(0, cast=int) or None
        student_id = (request.args(1) != None) and request.args(1, cast=int) or None
        parent_id = auth.user_id
        query = (db.auth_user.id == parent_id)
        parent_name = db(query).select(db.auth_user.first_name, db.auth_user.last_name)
        for row in parent_name:
            parent_name = row.first_name + " " + row.last_name
            
        query = ((db.parent_student.student_id == student_id) &
                 (db.parent_student.parent_id == parent_id) &
                 (db.student.id == student_id))
        
        student_id_list = db(query).select(db.student.id, db.student.user_id)
        student_auth_id = 0
        for student in student_id_list:
            student_auth_id = student.user_id
        query = ((db.student.user_id == student_auth_id) &
                 (db.auth_user.id == db.student.user_id))
        student_name = db(query).select(db.auth_user.first_name, db.auth_user.last_name)
        student_name = student_name[0]
        name = student_name.first_name + " " + student_name.last_name
        
        class_name = get_class_name(class_id).name

        assignment_query = get_student_assignment_list(student_id, class_id)

        #[name, score, possible_score, precent, due]
        assignment_data = []
        assignment_count = 0
        for row in assignment_query:
            precent = float(row.student_grade.student_score / row.grade.score *100)
            is_due = ""
            if (row.grade.due_date > datetime.datetime.now()):
                is_due = "warning"
            else:
                is_due = "success"
            assignment = [row.grade.name, row.student_grade.student_score, row.grade.score, precent, "{:%b %d, %Y}".format(row.grade.due_date), is_due]
            assignment_count +=1
            assignment_data.append(assignment)

        return dict(name=name, class_name=class_name, assignment_data=assignment_data, parent_name=parent_name, student_id=student_id, student_auth_id=student_auth_id,student_id_list=student_id_list, class_id=class_id, assignment_count = assignment_count)
    else:
        return dict(redirect(URL('default','index')))


    for student in student_ids:
        #set up query to pull back classes a student is in.
        student_classes_query = ((db.student.id==student.id)&
                                 (db.student.id == db.student_classes.student_id)&                                                (db.student_classes.class_id==db.classes.id))

        student_classes = db(student_classes_query).select(db.classes.id, db.classes.name)

        student_name = get_student_name(student.user_id)
        name = student_name.first_name + " " + student_name.last_name
        student_name_dict[student.id] = name
        student_class_and_average_dict = {}
        i = 0
        class_dict = {}

        for student_class in student_classes:
            student_average_list = get_student_assignment_average(student.id, student_class.id)
            student_average = format(float((student_average_list[0]/student_average_list[1] * 100)), '.2f')
            i += 1
            
            student_standards = student_standards_query(student.id, student_class.id)
            
            standard_info = db(student_standards).select(db.standard.id, db.standard.short_name, db.standard.reference_number,db.student_grade.student_score, db.grade.score,orderby=db.standard.id)
            #create empty standard dictionary
            standard_dict={}
            #for each row returned by the query...
            for row in standard_info:
                #if the standard is already in the dictionary...
                if row.standard.id in standard_dict.keys():
                    #make sure neither score is zero (error avoidance)
                    if((row.grade.score != 0.0) | (row.student_grade.student_score != 0.0)):
                        #set max score to the current standard cumulative score plus whatever the score is for the row
                        max_score = standard_dict[row.standard.id][0] + row.grade.score
                        #set new student score in the same basic way
                        student_score = standard_dict[row.standard.id][1] +                                                                         row.student_grade.student_score
                        #overwrite the standard to have [new max score, new student score, ref num and short name
                        standard_dict[row.standard.id] = [max_score, student_score,                                                                     row.standard.reference_number,                                                                 row.standard.short_name]
                else:
                    #otherwise, add the key to the dictionary with the information.
                    standard_dict[row.standard.id] = [row.grade.score,
                                                      row.student_grade.student_score,
                                                      row.standard.reference_number,
                                                      row.standard.short_name]

            class_dict[student_class.name] = [student_average, standard_dict, student_class.id]
            full_dict[student.id] = [name, class_dict]


    return dict(full_dict=full_dict,
                 parent_name=parent_name,
               class_id=class_id,
               student_id=student_id)

@auth.requires_login()
def overview():
    if auth.has_membership(4, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))
    parent_id = auth.user_id
    query = (db.auth_user.id == parent_id)
    parent_name = db(query).select(db.auth_user.first_name, db.auth_user.last_name)
    for row in parent_name:
        parent_name = row.first_name + " " + row.last_name
    #setup query of students linked to the parent_id
    student_ids_query = ((db.auth_user.id == parent_id) &
                         (db.auth_user.id == db.parent_student.parent_id) &
                         (db.parent_student.student_id == db.student.id))
    student_ids = db(student_ids_query).select(db.student.id, db.student.user_id)
    student_id_dict = {}
    student_name_dict = {}
    full_dict = {}
    
    for student in student_ids:
        #set up query to pull back classes a student is in.
        student_classes_query = ((db.student.id==student.id)&
                                 (db.student.id == db.student_classes.student_id)&                                                (db.student_classes.class_id==db.classes.id))
    
        student_classes = db(student_classes_query).select(db.classes.id, db.classes.name)
        
        student_name = get_student_name(student.user_id)
        name = student_name.first_name + " " + student_name.last_name
        student_name_dict[student.id] = name
        student_class_and_average_dict = {}
        i = 0
        class_dict = {}
        
        for student_class in student_classes:
            student_average_list = get_student_assignment_average(student.id, student_class.id)
            student_average = format(float((student_average_list[0]/student_average_list[1] * 100)), '.2f')
            i += 1
            
            student_standards = student_standards_query(student.id, student_class.id)
            
            standard_info = db(student_standards).select(db.standard.id, db.standard.short_name, db.standard.reference_number,db.student_grade.student_score, db.grade.score,orderby=db.standard.id)
            #create empty standard dictionary
            standard_dict={}
            #for each row returned by the query...
            for row in standard_info:
                #if the standard is already in the dictionary...
                if row.standard.id in standard_dict.keys():
                    #make sure neither score is zero (error avoidance)
                    if((row.grade.score != 0.0) | (row.student_grade.student_score != 0.0)):
                        #set max score to the current standard cumulative score plus whatever the score is for the row
                        max_score = standard_dict[row.standard.id][0] + row.grade.score
                        #set new student score in the same basic way
                        student_score = standard_dict[row.standard.id][1] +                                                                         row.student_grade.student_score
                        #overwrite the standard to have [new max score, new student score, ref num and short name
                        standard_dict[row.standard.id] = [max_score, student_score,                                                                     row.standard.reference_number,                                                                 row.standard.short_name]
                else:
                    #otherwise, add the key to the dictionary with the information.
                    standard_dict[row.standard.id] = [row.grade.score,
                                                      row.student_grade.student_score,
                                                      row.standard.reference_number,
                                                      row.standard.short_name]

            
            class_dict[student_class.name] = [student_average, standard_dict, student_class.id]
            full_dict[student.id] = [name, class_dict]


    return dict(full_dict=full_dict,
                 parent_name=parent_name)
'''
#####################################################
#####################################################
'''

def pdf_overview():

    #get arguments passed from previous page
    student_id = (request.args(0) != None) and request.args(0, cast=int) or None
    class_id = (request.args(1) != None) and request.args(1, cast=int) or None
    assignment_count = (request.args(2) != None) and request.args(2, cast=int) or None
    
    query = (db.student.id == student_id)
    student_user_id = 0
    user_ids = db(query).select(db.student.user_id)
    for i in user_ids:
        student_user_id = i.user_id
    '''
    Grade_standard_dict----
    '''
    query=((db.classes.id==class_id)&
           (db.classes.id==db.class_grade.class_id)&
           (db.class_grade.grade_id==db.grade.id)&
           (db.grade.id==db.grade_standard.grade_id)&
           (db.grade_standard.standard_id==db.standard.id))
    grade_standard = db(query).select(db.grade.id, db.grade.name, db.standard.id)

    grade_standard_dict={}
    for row in grade_standard:
        if row.grade.id in grade_standard_dict.keys():
            grade_standard_dict[row.grade.id][1].append(row.standard.id)
        else:
            grade_standard_dict[row.grade.id] = [row.grade.name, [row.standard.id]]
            
            
    '''
    Grade_Student_dict------
    '''
    query = ((db.classes.id==class_id)&
             (db.classes.id==db.class_grade.class_id)&
             (db.class_grade.grade_id==db.grade.id)&
             (db.grade.id==db.student_grade.grade_id)&
             (db.student_grade.student_id==db.student.id)&
            (db.student.id == student_id))

    student_grades = db(query).select(db.grade.id, db.grade.name, db.grade.score, db.student_grade.student_score)

    grade_student_dict={}
    for row in student_grades:
        if row.grade.id in grade_student_dict.keys():
            if((row.grade.score != 0.0) | (row.student_grade.student_score != 0.0)):
                max_score = grade_student_dict[row.grade.id][0] + row.grade.score
                student_score = grade_student_dict[row.grade.id][1] + row.student_grade.student_score
                grade_student_dict[row.grade.id] = [max_score, student_score, row.grade.name]
        else:
            if((row.grade.score != 0.0) | (row.student_grade.student_score != 0.0)):
                grade_student_dict[row.grade.id] = [row.grade.score, row.student_grade.student_score, row.grade.name]
            
            
    '''
    Line Graph stuff
    '''
    assignment_query = get_student_assignment_list(student_id, class_id)
    assignment_data = []
    assignment_names = []
    assignment_line_all = [[]]
    assignment_count = 0
    tup2 = ()
    i = 0
    for row in assignment_query:
        precent = float(row.student_grade.student_score / row.grade.score *100)
        assignment = [row.grade.name, row.student_grade.student_score, row.grade.score, precent, "{:%b %d, %Y}".format(row.grade.due_date)]
        tup1 = (row.grade.score,)
        assignment_names.append(row.grade.name)
        assignment_line_all[0].append(precent)
        assignment_data.append(assignment)
        assignment_count+=1
    
            
    '''
    TEST
    '''
    query = ((db.classes.id == class_id) &
             (db.class_grade.class_id == db.classes.id) &
             (db.class_grade.grade_id == db.grade.id) &
             (db.grade.id == db.student_grade.grade_id ) &
             (db.student_grade.student_id == db.student.id ) &
             (db.student.id == student_id) &
             (db.grade.due_date != None))

    student_assignment = db(query).select(db.grade.id, db.grade.name, db.grade.score, db.student_grade.student_score)

    assignment_dict = {}
    for row in student_assignment:
        if row.student_grade.student_score != 0:
            assignment_dict[row.grade.id] = [row.grade.name, round(row.student_grade.student_score / row.grade.score * 100, 2), get_assignment_class_average(class_id,row.grade.id)]
        elif row.student_grade.student_score == 0:
            assignment_dict[row.grade.id] = [row.grade.name, 0, get_assignment_class_average(class_id,row.grade.id)]

    sorted_assignment_dict = collections.OrderedDict(sorted(assignment_dict.items()))
    assignment_dict = sorted_assignment_dict
            
            
            
    #get a pdf from the helper function
    pdf = create_single_grade_pdf(student_id,student_user_id, class_id, assignment_count, grade_standard_dict, grade_student_dict, assignment_line_all, assignment_names, assignment_dict)
    return pdf

def create_single_grade_pdf(student_id,student_user_id, class_id, assignment_count, grade_standard_dict, grade_student_dict, assignment_line_all, assignment_names, assignment_dict):
    '''--Variables--'''
    Story=[]
    Elements=[]
    buff = StringIO()
    formatted_time = time.ctime()
    minimum = 100
    standard_averages=[[]]
    standard_table=[]

    #content_areas = []

    '''------'''
    styles = getSampleStyleSheet()
    HeaderStyle = styles["Heading1"]

    #get the student Name

    #Create the name for the PDf being returned
    pdfName = get_student_name(student_user_id).first_name+"_"+get_student_name(student_user_id).last_name+"_SR"+".pdf"

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
                                  #alignment = TA_LEFT,
                                  spaceAfter = 6),
                                  alias = 'title2')


    #Time-Stamp
    ptext = '<font size=12>%s</font>' % formatted_time
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    Elements.extend(ptext)

    #Administrator
    ptext='<font size=12><b>%s %s</b></font>'%(get_student_name(student_user_id).first_name, get_student_name(student_user_id).last_name)
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))
    Elements.extend(ptext)

    #Grade Number and Content Area
    ptext = '<font size=12><b>%s Student Report</b></font>'%(get_class_name(class_id).name)
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 7))
    Elements.extend(ptext)
    
    
    #Total Assignments
    ptext = '<font size=12>Total Assignments: %s</font>'%(assignment_count)
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 7))
    Elements.extend(ptext)
    
    
    
    
    
    Story.append(Spacer(1,20))
    #Graph Title
    ptext = '<font size=15><b>Current Performance by Standard</b></font>'
    Story.append(Paragraph(ptext, styles["title"]))
    Story.append(Spacer(1,50))

    
    #get all the standards for a specific grade and content area
    standard_query = ((db.classes.id == class_id)&
                       (student_id == db.student.id)&
                      (db.classes.id == db.student_classes.class_id)&
                      (db.student.id == db.student_classes.student_id)&
                      (db.student.id == db.student_grade.student_id)&
                      (db.grade.id == db.student_grade.grade_id)&
                      (db.grade.id == db.grade_standard.grade_id)&
                      (db.standard.id == db.grade_standard.standard_id)&
                      (db.classes.id == db.class_grade.class_id)&
                      (db.grade.id == db.class_grade.grade_id)&
                      (db.standard.content_area == db.contentarea.id))

    standard_list = db(standard_query).select(db.standard.id, db.standard.short_name, db.standard.reference_number,db.student_grade.student_score, db.grade.score, db.contentarea.name)
    standard_ref_list=[]
    #Setup the Dictionary of standard averages
    standard_dict = {}
    standard_table = []
    standard_averages=[[]]
    for row in standard_list:
        if row.standard.id in standard_dict.keys():
            if((row.grade.score != 0.0) | (row.student_grade.student_score != 0.0)):
                max_score = standard_dict[row.standard.id][0] + row.grade.score
                student_score = standard_dict[row.standard.id][1] + row.student_grade.student_score
                standard_dict[row.standard.id] = [max_score, student_score, row.standard.reference_number, row.standard.short_name]
        else:
            standard_dict[row.standard.id] = [row.grade.score, row.student_grade.student_score, row.standard.reference_number, row.standard.short_name]

    
    
        
    i = 0
    #set up the 2D list of Standard Averages
    for standard in sorted(standard_dict.keys()):
        standard_ref_list.append(standard_dict[standard][2])
        standard_table.append([])
        current_avg = (standard_dict[standard][1]/standard_dict[standard][0])*100
        if minimum > current_avg:
            minimum = current_avg
        #int/round was here
        standard_table[i].append(standard_dict[standard][3]+": "+format((standard_dict[standard][1]/standard_dict[standard][0])*100,'.2f')+"%")
        #int/round was here 
        standard_averages[0].append((standard_dict[standard][1]/standard_dict[standard][0])*100)


        for grade in grade_standard_dict.keys():
            for standardId in grade_standard_dict[grade][1]:
                if(standardId == standard):
                    standard_table[i].append(grade_standard_dict[grade][0]+":"+format((grade_student_dict[grade][1]/grade_student_dict[grade][0])*100, '.2f')+"%")
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
    bc.barLabelFormat = '%.2f%%'
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
    Story.append(Spacer(1,15))
    #LineGraph Title
    ptext = '<font size=15><b>Class Performance by Assignment</b></font>'
    Story.append(Paragraph(ptext, styles["title"]))
    Story.append(Spacer(1,30))
    
    '''
    Line Plot Graph ------
    '''
    assignment_data_all =[[],[]]
    for key in assignment_dict.keys():
        assignment_data_all[0].append(assignment_dict[key][2])
        assignment_data_all[1].append(assignment_dict[key][1])
    drawing2 = Drawing(600, 200)
    data2 = assignment_data_all
    #lp = LinePlot()
    
    #data[0] = preprocessData(data[0])
    lp = HorizontalLineChart()
    lp.x = -20
    lp.y = 0
    lp.height = 225
    lp.width = 500
    lp.data = data2
    lp.joinedLines = 1
    lp.lines.symbol = makeMarker('FilledCircle')
    lp.lines[0].strokeColor = colors.grey
    lp.lines[1].strokeColor = colors.lightblue
    lp.strokeColor = colors.black
    lp.categoryAxis.labels.fontSize = 7
    lp.categoryAxis.categoryNames = assignment_names
    lp.categoryAxis.labels.boxAnchor = 'ne'
    lp.categoryAxis.labels.angle = 30
    lp.categoryAxis.drawGridLast=True
    #lp.categoryAxis.gridStart=0
    lp.categoryAxis.gridStrokeLineCap = 2
    #lp.categoryAxis.gridEnd=3
    #lp.categoryAxis.visibleGrid           = 1
    lp.valueAxis.visibleGrid           = 1
    lp.valueAxis.visible               = 1
    lp.valueAxis.drawGridLast=False
    #lp.valueAxis.gridStart = 0
    #lp.valueAxis.gridEnd = 100
    lp.valueAxis.gridStrokeColor = colors.black
    lp.valueAxis.valueMin = 0
    lp.valueAxis.valueMax = 105
    lp.valueAxis.valueStep = 10
    lp.lineLabelFormat = '%2.0f'
    lp.strokeColor = colors.black
    lp.fillColor = colors.white
    drawing2.add(lp)
    
    legend = Legend()
    legend.alignment = 'right'
    legend.x = 482
    legend.y = 150
    legend.deltax = 60
    legend.dxTextSpace = 2
    legend.colorNamePairs = [(colors.lightblue, 'Student'),(colors.grey, 'Class')]
    drawing2.add(legend, 'legend')
    
    Story.append(drawing2)
    Story.append(Spacer(1,30))
    ptext = '<font size=15><b>Assignments by Standard</b></font>'
    Story.append(Paragraph(ptext, styles["title"]))
    Story.append(Spacer(1,10))
    t=Table(standard_table)
    t.setStyle(t.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                      ('FONTSIZE', (0,0), (-1,-1), 7),
                                      ('BACKGROUND',(0,0),(0,-1),colors.lightgrey),
                                      ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),])))
    Story.append(t)
    #build PDF document and return it
    doc.build(Story)
    pdf = buff.getvalue()
    buff.close()
    return pdf
