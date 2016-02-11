"""
A controller to generate all of the charts we'll be using.
"""

import gluon.contrib.simplejson as json


@auth.requires(auth.has_membership(role='Teacher'), requires_login=True)
def standards_performance_for_teacher():
    """
    Overall performance across all classes by standard.
    """

    query = ((db.gradebook.teacher==auth.user_id) &
             (db.gradebook.classes==db.classes.id) &
             (db.class_grade.class_id==db.classes.id) &
             (db.class_grade.grade_id==db.grade.id) &
             (db.student_grade.grade_id==db.grade.id) &
             (db.grade.id==db.grade_standard.grade_id) &
             (db.standard.id==db.grade_standard.standard_id))

    standard_list = db(query).select(db.standard.short_name,
                                     db.student_grade.student_score.sum(),
                                     db.grade.score.sum(),
                                     orderby=db.standard.reference_number,
                                     groupby=db.standard.reference_number)

    standard_data = {
        'label': [],
        'data': []
    }

    for standard in standard_list:
        standard_data['label'].append(standard.standard.short_name)
        standard_data['data'].append((standard['SUM(student_grade.student_score)'] / standard['SUM(grade.score)']) * 100)

    return dict(standard_data=standard_data)



def class_overview_pie():
    class_id = (request.args(0) != None) and request.args(0, cast=int) or None
    total_score = get_class_total_score(class_id)
    total_possible= get_class_total_possible(class_id)
    average = 0
    try:
        average = round(total_score / total_possible * 100.0, 2)
    except:
        pass

    return dict(average=average)

def class_overview_percent_range_pie():
    class_id = (request.args(0) != None) and request.args(0, cast=int) or None
    teacher_id = auth.user_id
    query = ((db.classes.id == class_id)&
             (db.classes.id == db.class_grade.class_id)&
             (db.grade.id == db.class_grade.grade_id)&
             (db.classes.id == db.student_classes.class_id)&
             (db.student.id == db.student_classes.student_id)&
             (db.student.id == db.student_grade.student_id)&
             (db.grade.id == db.student_grade.grade_id))

    grade = db(query).select(db.student.id, db.student_grade.student_score, db.grade.score)

    assignment_query = {}
    for row in grade:
        if row.student.id in assignment_query.keys():
            total_score = assignment_query[row.student.id][1] + row.grade.score
            student_score = assignment_query[row.student.id][0] + row.student_grade.student_score
            assignment_query[row.student.id] = [student_score, total_score]
        else:
            assignment_query[row.student.id] = [row.student_grade.student_score, row.grade.score]

    pie_data = {}
    pie_data[90] = 0
    pie_data[80] = 0
    pie_data[70] = 0
    pie_data[60] = 0
    pie_data[50] = 0
    for key in assignment_query.keys():
        average = assignment_query[key][0] / assignment_query[key][1] *100
        if average >= 90:
            pie_data[90] = pie_data[90]+1
        elif average >= 80 and average < 90:
            pie_data[80] = pie_data[80]+1
        elif average >= 70 and average < 80:
            pie_data[70] = pie_data[70]+1
        elif average >= 60 and average < 70:
            pie_data[60] = pie_data[60]+1
        else:
            pie_data[50] = pie_data[50]+1

    return dict(pie_data=pie_data)


def class_overview_assignment_range_pie():
    class_id = (request.args(0) != None) and request.args(0, cast=int) or None
    teacher_id = auth.user_id
    query = ((db.classes.id == class_id)&
             (db.classes.id == db.class_grade.class_id)&
             (db.grade.id == db.class_grade.grade_id)&
             (db.classes.id == db.student_classes.class_id)&
             (db.student.id == db.student_classes.student_id)&
             (db.student.id == db.student_grade.student_id)&
             (db.grade.id == db.student_grade.grade_id))

    grade = db(query).select(db.grade.id, db.student_grade.student_score, db.grade.score)

    assignment_query = {}
    for row in grade:
        if row.grade.id in assignment_query.keys():
            total_score = assignment_query[row.grade.id][1] + row.grade.score
            student_score = assignment_query[row.grade.id][0] + row.student_grade.student_score
            assignment_query[row.grade.id] = [student_score, total_score]
        else:
            assignment_query[row.grade.id] = [row.student_grade.student_score, row.grade.score]


    pie_data = {}
    pie_data[90] = 0
    pie_data[80] = 0
    pie_data[70] = 0
    pie_data[60] = 0
    pie_data[50] = 0

    for key in assignment_query.keys():
        average = assignment_query[key][0] / assignment_query[key][1] *100
        if average >= 90:
            pie_data[90] = pie_data[90]+1
        elif average >= 80 and average < 90:
            pie_data[80] = pie_data[80]+1
        elif average >= 70 and average < 80:
            pie_data[70] = pie_data[70]+1
        elif average >= 60 and average < 70:
            pie_data[60] = pie_data[60]+1
        else:
            pie_data[50] = pie_data[50]+1

    for key in pie_data.keys():
        print("key: ", key)
        print(pie_data[key])


    return dict(pie_data=pie_data)




def class_overview_standard_bar():

    class_id = (request.args(0) != None) and request.args(0, cast=int) or None
    teacher_id = auth.user_id

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


    return dict(standard_dict=standard_dict)






def chart():
    return dict()


# This only exists because "index" is the default function.
@auth.requires_login()
def index(): redirect(URL('default', 'index'))
