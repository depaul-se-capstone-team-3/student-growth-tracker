"""
The classes controller.

Everything concerning classes goes here. Sort of. We'll clarify as we go on.
"""

from gluon.contrib.simplejson import dumps, loads
import datetime
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from operator import itemgetter
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.widgets.grids import ShadedRect
from reportlab.graphics.shapes import Drawing

@auth.requires_login()
def index():
    if auth.has_membership(3, auth.user_id):
        pass
    elif auth.has_membership(2,auth.user_id):
        pass
    else:
        redirect(URL('default','index'))
    """
    Display the list of classes associated with the logged in user.

    - If the user is a teacher, the list shows all of the classes that teacher
      teaches.
    - If the user is a student, the list shows all of the classes that student
      attends.

    .. todo:: Make these queries context sensitive per the list in the docstring.
              They should also have generic names, but I think the ones I chose
              are probably good, at least for now.

    .. todo:: Add checks to determine user role, and select appropriate query.
    """

    teacher_id = auth.user_id # Cache the user id of the logged-in teacher
                              # to make it easier to access and recognize.

    class_id = (request.args(0) != None) and request.args(0, cast=int) or None

    ############################################################################
    ## This should go into a function.
    if not class_id:
        response.flash = T("Class Does Not Exist")
        session.flash = T("Class does not exist.")

        # Redirect to previous link if via link, else redirect to main page.
        if (request.env.http_referer==None):
            redirect(URL('default', 'index'))
        else:
            redirect(request.env.http_referer)
    ##
    ############################################################################

    class_name = db.classes[class_id].name
    class_list = get_class_list(teacher_id)
    class_roster = get_class_roster(teacher_id, class_id)
    class_assignments = get_class_assignments(teacher_id, class_id)
    assignments = get_student_assignments(teacher_id, class_id)
    standards = get_standards_for_class(class_id)
    
    return dict(class_id=class_id,
                class_name=class_name,
                class_list=class_list,
                class_roster=class_roster,
                class_assignments=class_assignments,
                assignments=assignments,
                standards=standards)

@auth.requires_login()
def student_grades():
    if auth.has_membership(2, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))
    """
    Retrieves grade information for a given ``class_id``
    and returns it as ``json``.
    """
    teacher_id = auth.user_id
    class_id = (request.args(0) != None) and request.args(0, cast=int) or None
    standard_id = (request.args(1) != None) and request.args(1, cast=int) or None

    assignments = []

    class_assignments = get_class_assignments(teacher_id, class_id, standard_id)
    hdr_row = [None, None]
    date_row = [None, None]
    score_row = [None, None]
    
    for assignment in class_assignments:
        hdr_row += [None, assignment.name]
        due_date = assignment.due_date and assignment.due_date.strftime(DATE_FORMAT) or None
        date_row += [None, due_date]
        score_row += [None, assignment.score]

    assignments.append(hdr_row)
    assignments.append(date_row)
    assignments.append(score_row)
    assignments += (get_student_assignments(teacher_id,
                                            class_id,
                                            standard_id))

    return dumps(assignments)

@auth.requires_login()
def save_student_grades():
    if auth.has_membership(3, auth.user_id):
        pass
    elif auth.has_membership(2,auth.user_id):
        pass
    else:
        redirect(URL('default','index'))
    """
    Receives ``json`` data via ajax from the ``handsontable`` object
    and saves it back to the database.

    In this incarnation, all data is saved to the database regardless of if it
    has changed. This needs to be fixed so that only the changed data is saved.
    I need to check what parameters are sent to the relevant ``handsontable``
    function.
    """
    vargs = request.vars

    for k in vargs.keys():
        student_grades = vargs[k]
        for i in range(2, len(student_grades), 2):
            try:
                grade_id = int(student_grades[i])
                score = float(student_grades[i+1])
                db.student_grade[grade_id] = dict(student_score=score)
            except Exception as e:
                # Don't save the value, but the client side validation
                # should warn the user, so DRY.
                pass

    return dumps(dict()) # Return nothing, but make sure it's in json format.

@auth.requires_login()
def assignment_info():
    if auth.has_membership(2, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))
    teacher_id = auth.user_id
    class_id = (request.args(0) != None) and request.args(0, cast=int) or None
    standard_id = (request.args(1) != None) and request.args(1, cast=int) or None

    return dumps(get_class_assignments(teacher_id, class_id, standard_id).as_list())

@auth.requires_login()
def overview():
    if auth.has_membership(2, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))
    teacher_id = auth.user_id
    #Class ID
    class_id = (request.args(0) != None) and request.args(0, cast=int) or None

    #Teacher Name
    teacher_name = get_teacher_name(teacher_id)
    
    #Class Name
    query = teacher_classes_query(teacher_id, class_id)
    class_query = db(query).select(db.classes.name)
    class_name = class_query[0].name
    
    
    #To display number of students.
    total_students = len(get_class_roster(teacher_id, class_id))

    #To display number of assignments
    grade_query = ((db.class_grade.class_id == class_id) &
                   (db.class_grade.grade_id == db.grade.id))
    total_grades = db(grade_query).count()

    #To display class average
    total_score = get_class_total_score(class_id)
    total_possible= get_class_total_possible(class_id)
    average = 0
    try:
        average = round(total_score / total_possible * 100.0, 2)
    except:
        pass

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
        
    #To display due soon
    due_soon_amount = 3

    #Need to filter with current day datetime.datetime.now()
    due_soon_query = ((db.classes.id==class_id) &
             (db.gradebook.teacher==teacher_id) &
             (db.gradebook.classes==db.classes.id) &
             (db.class_grade.class_id==db.classes.id) &
             (db.class_grade.grade_id==db.grade.id) &
             (db.grade.due_date != None) &
             (db.grade.due_date > datetime.datetime.now()))

    due_soon = db(due_soon_query).select(db.grade.name, db.grade.due_date,orderby=db.grade.due_date)

    #If number of assignment is less than the number we want to display
    if(len(due_soon) < due_soon_amount):
        due_soon_amount = len(due_soon)

    return dict(class_name=class_name,
                class_id=class_id,
                total_students=total_students,
                total_grades=total_grades,
                total_score=total_score,
                total_possible=total_possible,
                average=average,
                standard_dict=standard_dict,
                due_soon=due_soon,
                due_soon_amount=due_soon_amount)

@auth.requires_login()
def pdf_overview():
    if auth.has_membership(2, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))

    teacher_id = auth.user_id
    #Class Id
    class_id = (request.args(0) != None) and request.args(0, cast=int) or None

    #To display class name.
    query = teacher_classes_query(teacher_id, class_id)
    class_query = db(query).select(db.classes.name)
    class_name = class_query[0].name

    #Teacher Name
    teacher_name = get_teacher_name(teacher_id)

    #To display number of students.
    total_students = len(get_class_roster(teacher_id, class_id))

    #To display number of assignments
    grade_query = ((db.class_grade.class_id == class_id) &
                   (db.class_grade.grade_id == db.grade.id))
    total_grades = db(grade_query).count()

    #To display class average
    total_score = get_class_total_score(class_id)
    total_possible= get_class_total_possible(class_id)
    class_average = 0
    try:
        class_average = round(total_score / total_possible * 100.0, 2)
    except:
        pass

    '''
    GRADE STANDARDS---------------------------------
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
    ASSIGNMENT AVERAGES-------------------------------
    '''
    query = ((db.classes.id==class_id)&
             (db.classes.id==db.class_grade.class_id)&
             (db.class_grade.grade_id==db.grade.id)&
             (db.grade.id==db.student_grade.grade_id)&
             (db.student_grade.student_id==db.student.id))

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
    STANDARD AVERAGES--------------------------
    '''
    query = ((db.classes.id==class_id) &
             (db.class_grade.class_id==class_id) &
             (db.class_grade.grade_id==db.grade.id) &
             (db.student_grade.grade_id==db.grade.id) &
             (db.grade.id==db.grade_standard.grade_id) &
             (db.standard.id==db.grade_standard.standard_id) &
             (db.standard.content_area == db.contentarea.id))
    standards_list=[]
    standard_list = db(query).select(db.standard.id, db.standard.short_name, db.standard.reference_number,db.student_grade.student_score, db.grade.score)

    standard_total_dict = {}
    for row in standard_list:
        if row.standard.id in standard_total_dict.keys():
            if((row.grade.score != 0.0) | (row.student_grade.student_score != 0.0)):
                max_score = standard_total_dict[row.standard.id][0] + row.grade.score
                student_score = standard_total_dict[row.standard.id][1] + row.student_grade.student_score
                standard_total_dict[row.standard.id] = [max_score, student_score, row.standard.reference_number, row.standard.short_name]
        else:
            standards_list.append(row.standard.reference_number)
            standard_total_dict[row.standard.id] = [row.grade.score, row.student_grade.student_score, row.standard.reference_number, row.standard.short_name]

    #create a pdf for this class overview
    create_single_class_pdf(teacher_name, class_id, class_name, class_average, total_students, total_grades,standards_list, grade_standard_dict, grade_student_dict, standard_total_dict)

    #Make sure no one stays on this page. if everything passes above, then they are booted back to their default index screen. 
    #WHEN IS THIS USED: if the user manually types the url above. if they go by way of a button, the pdf_creation Function redirects them
    #to the page they were originally on.
    redirect(URL('default','index'))

def create_single_class_pdf(teacher_name, class_id,class_name, class_average, total_students, total_grades, standards_list, grade_standard_dict, grade_student_dict, standard_total_dict):
    styles = getSampleStyleSheet()
    HeaderStyle = styles["Heading1"]
    doc = SimpleDocTemplate(class_name+"_CLR"+".pdf",pagesize=letter,rightMargin=72,leftMargin=72,topMargin=72,bottomMargin=18)
    Story=[]
    Elements=[]
    formatted_time = time.ctime()
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

    ptext = '<font size=12>%s</font>' % formatted_time

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    Elements.extend(ptext)

    #Teacher Name
    ptext='<font size=12><b>%s %s</b></font>'%(teacher_name.first_name, teacher_name.last_name)
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))
    Elements.extend(ptext)

    #Class Name
    ptext = '<font size=12>%s: </font>'%(class_name)
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 7))
    Elements.extend(ptext)

    #Class Average
    ptext = '<font size=12>Class Average:%s%%</font>'%(class_average)
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1,12))
    Elements.extend(ptext)

    #Total Students
    ptext = '<font size=12>Total Students:%s</font>'%(total_students)
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1,12))
    Elements.extend(ptext)

    #Total Assignments
    ptext = '<font size=12>Total Assignments:%s</font>'%(total_grades)
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1,12))
    Story.append(Spacer(1,40))

    ptext = '<font size=15><b>Standards Progress</b></font>'
    Story.append(Paragraph(ptext, styles["title"]))

    test_values=[[10,20,50,90,80]]
    standard_table=[]
    i = 0
    standard_averages=[[]]
    #Go through the standard_total_dict keys and add all the necessary values to the standard_averages 2d list.
    for standard in standard_total_dict.keys():
        standard_table.append([])
        standard_table[i].append(standard_total_dict[standard][3]+": "+format((standard_total_dict[standard][1]/standard_total_dict[standard][0])*100,'.2f')+"%")
        standard_averages[0].append(int(round((standard_total_dict[standard][1]/standard_total_dict[standard][0])*100)))

        #add assignments to correct buckets
        for grade in grade_standard_dict.keys():
            for standardId in grade_standard_dict[grade][1]:
                if(standardId == standard):
                    standard_table[i].append(grade_standard_dict[grade][0]+":"+format((grade_student_dict[grade][1]/grade_student_dict[grade][0])*100, '.2f')+"%")
        i+=1
    sorted(standard_table,key=lambda l:l[0])

    #graph
    drawing = Drawing(600, 200)
    data = standard_averages
    bc = VerticalBarChart()

    #location in the document (x,y)
    bc.x = 50
    bc.y = 50

    #width and height of the graph
    bc.height = 125
    bc.width = 300
    bc.data = data

    bc.barLabels = [10,20,30,40,50]

    #Update colors of the bars in the graph
    bc.bars.symbol = ShadedRect()
    bc.bars.symbol.fillColorStart = colors.blue
    bc.bars.symbol.fillColorEnd = colors.blue
    bc.bars.symbol.strokeWidth = 0


    #this draws a line at the top of the graph to close it. 
    bc.strokeColor = colors.black

    #Y-axis min, max, and steps. 
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 100
    bc.valueAxis.valueStep = 10

    #where to anchor the origin of the graph
    bc.categoryAxis.labels.boxAnchor = 'ne'

    #Locations of labels for the X-axis
    bc.categoryAxis.labels.dx = 2
    bc.categoryAxis.labels.dy = -2

    #The angle of the lables for the X-axis
    bc.categoryAxis.labels.angle = 30
    #List of the categories to place on the X-axis
    bc.categoryAxis.categoryNames = standards_list
    drawing.add(bc)

    #Graph Legend
    legend = Legend()
    legend.alignment = 'right'
    legend.x = 355
    legend.y = 150
    legend.deltax = 60
    legend.dxTextSpace = 10
    legend.columnMaximum = 4

    legend.colorNamePairs = [(colors.blue, 'grade average')]
    drawing.add(legend, 'legend')
    drawing_title = "Bar Graph"

    Story.append(drawing)
    
    #drawing.save(fnRoot='example', formats=['png', 'pdf'])

    t=Table(standard_table)
    t.setStyle(t.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                      ('FONTSIZE', (0,0), (-1,-1), 7),
                                      ('BACKGROUND',(0,0),(0,-1),colors.lightgrey),
                                      ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),])))
    Story.append(t)
    
    doc.build(Story)
    redirect(request.env.http_referer)
