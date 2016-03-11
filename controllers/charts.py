"""
A controller to generate all of the charts we'll be using.
"""

import gluon.contrib.simplejson as json
import collections


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
    for key in assignment_query.keys():
        average = assignment_query[key][0] / assignment_query[key][1] *100
        if average >= 90:
            pie_data[90] = pie_data[90]+1
        elif average >= 70 and average < 90:
            pie_data[80] = pie_data[80]+1
        else:
            pie_data[70] = pie_data[70]+1

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

    sorted_standard_dict = collections.OrderedDict(sorted(standard_dict.items()))
    standard_dict = sorted_standard_dict


    return dict(standard_dict=standard_dict)

def admin_standard_overview_bar():
    key = (request.args(0) != None) and request.args(0, cast=int) or None
    grade_query = ((db.classes.grade_level))
    grade = db(grade_query).select(db.classes.grade_level)
    grade_list = []
    for row in grade:
        grade_list.append(row.grade_level)
    grade_list = list(set(grade_list))
    #print(grade_list)

    overview_data = {}
    for grade in grade_list:
        standard_query = ((db.classes.grade_level == grade)&
                          (db.classes.id == db.student_classes.class_id)&
                          (db.student.id == db.student_classes.student_id)&
                          (db.student.id == db.student_grade.student_id)&
                          (db.grade.id == db.student_grade.grade_id)&
                          (db.grade.id == db.grade_standard.grade_id)&
                          (db.standard.id == db.grade_standard.standard_id)&
                          (db.classes.id == db.class_grade.class_id)&
                          (db.grade.id == db.class_grade.grade_id)&
                          (db.standard.content_area == db.contentarea.id))

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

        overview_data[grade] = standard_dict


    return dict(overview_data = overview_data, key=key)


def parent_index_line():
    class_id = (request.args(0) != None) and request.args(0, cast=int) or None
    student_id = (request.args(1) != None) and request.args(1, cast=int) or None

    student_query = ((db.student.id == student_id)&
                     (db.student.id == db.student_grade.student_id)&
                     (db.student_grade.grade_id == db.grade.id)&
                     (db.classes.id == class_id)&
                     (db.classes.id == db.class_grade.class_id)&
                     (db.class_grade.grade_id == db.grade.id)&
                     (db.grade.due_date != None)&
                     (db.grade.due_date <= datetime.datetime.now()))

    student_assignment = db(student_query).select(db.grade.id, db.grade.name, db.grade.score, db.student_grade.student_score)

    assignment_dict = {}
    for row in student_assignment:
        if row.student_grade.student_score != 0:
            assignment_dict[row.grade.id] = [row.grade.name, round(row.student_grade.student_score / row.grade.score * 100, 2), get_assignment_class_average(class_id,row.grade.id)]
        elif row.student_grade.student_score == 0:
            assignment_dict[row.grade.id] = [row.grade.name, 0, get_assignment_class_average(class_id,row.grade.id)]

    sorted_assignment_dict = collections.OrderedDict(sorted(assignment_dict.items()))
    assignment_dict = sorted_assignment_dict

    return dict(assignment_dict=assignment_dict)


def student_index_line():
    class_id = (request.args(0) != None) and request.args(0, cast=int) or None
    student_id = (request.args(1) != None) and request.args(1, cast=int) or None

    query = ((db.classes.id == class_id) &
             (db.class_grade.class_id == db.classes.id) &
             (db.class_grade.grade_id == db.grade.id) &
             (db.grade.id == db.student_grade.grade_id ) &
             (db.student_grade.student_id == db.student.id ) &
             (db.student.id == student_id) &
             (db.grade.due_date != None)&
            (db.grade.due_date <= datetime.datetime.now()))

    student_assignment = db(query).select(db.grade.id, db.grade.name, db.grade.score, db.student_grade.student_score)

    assignment_dict = {}
    for row in student_assignment:
        if row.student_grade.student_score != 0:
            assignment_dict[row.grade.id] = [row.grade.name, round(row.student_grade.student_score / row.grade.score * 100, 2), get_assignment_class_average(class_id,row.grade.id)]
        elif row.student_grade.student_score == 0:
            assignment_dict[row.grade.id] = [row.grade.name, 0, get_assignment_class_average(class_id,row.grade.id)]

    sorted_assignment_dict = collections.OrderedDict(sorted(assignment_dict.items()))
    assignment_dict = sorted_assignment_dict

    return dict(assignment_dict=assignment_dict)


def admin_standard_overview_detail_bar():
    grade_level = (request.args(0) != None) and request.args(0, cast=int) or None
    content_id = (request.args(1) != None) and request.args(1, cast=int) or None

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

    return dict(detail_data=detail_data)


def chart():
    return dict()


# This only exists because "index" is the default function.
@auth.requires_login()
def index(): redirect(URL('default', 'index'))
