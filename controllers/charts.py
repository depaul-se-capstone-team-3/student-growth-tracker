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


def chart():
    return dict()


# This only exists because "index" is the default function.
@auth.requires_login()
def index(): redirect(URL('default', 'index'))
