"""
db_02_functions.py
==================

This module contains functions that generate queries or return data sets
to be used in the **Student Growth Tracker** application.

Functions that return a :py:class:`Query <pydal.objects.Query>` object
have names that end with ``_query``.

Functions that return sets of values have names that start with ``get_``.
"""
import datetime

def teacher_classes_query(teacher_id, class_id=None):
    """
    Return a :py:class:`Query <pydal.objects.Query>` object that represents the
    set of classes associated with ``teacher_id``. If ``class_id`` is provided,
    only that class will be included in the :py:class:`Set <pydal.objects.Set>`.
    """
    query = ((db.gradebook.teacher==teacher_id) &
             (db.gradebook.classes==db.classes.id) &
             (db.classes.content_area==db.contentarea.id))

    if class_id:
        query &= (db.gradebook.classes==class_id)

    return query

def get_class_list(teacher_id):
    """
    Return a :py:class:`Rows <pydal.objects.Rows>` object containing the classes
    associated with the teacher.

    Each :py:class:`Row <pydal.objects.Row>` object has the following fields:

    - ``classes.id``
    - ``classes.name``
    - ``contentarea.id``
    - ``contentarea.name``
    """
    query = teacher_classes_query(teacher_id)
    result = db(query).select(db.classes.id, db.classes.name, db.contentarea.id,
                              db.contentarea.name)
    return result

def get_class_roster(teacher_id, class_id):
    """
    Return a :py:class:`list` of lists of students in the class
    with id ``class_id``. Each list item is a two-element list
    with the format::

        [student.id, auth_user.first_name + ' ' + auth_user.last_name]
    """
    query = (teacher_classes_query(teacher_id, class_id) &
             (db.classes.id==db.student_classes.class_id) &
             (db.student_classes.student_id==db.student.id) &
             (db.student.user_id==db.auth_user.id))
    results = db(query).select(db.student.id,
                               db.auth_user.first_name,
                               db.auth_user.last_name)

    class_roster = []
    for s in results:
        class_roster.append([int(s.student.id),
                             s.auth_user.first_name + ' ' + s.auth_user.last_name])

    return class_roster

def class_assignment_query(teacher_id, class_id):
    """
    Return a :py:class:`Query <pydal.objects.Query>` object that represents the
    set of assignments for a given class.
    """
    query = (teacher_classes_query(teacher_id, class_id) &
             (db.classes.id==db.class_grade.class_id) &
             (db.class_grade.grade_id==db.grade.id))

    return query

def get_class_assignments(teacher_id, class_id):
    """
    Return a :py:class:`Rows <pydal.objects.Rows>` object containing
    all of the assignments for the class with id ``class_id``, sorted
    by due date.

    Each :py:class:`Row <pydal.objects.Row>` object has the following fields:

    - ``grade.name``
    """
    query = class_assignment_query(teacher_id, class_id)

    class_assignments = db(query).select(db.grade.name, db.grade.score, db.grade.due_date,
                                         orderby=db.grade.due_date)

    return class_assignments

def get_student_assignments(teacher_id, class_id):
    """
    Returns a :py:class:`list` of lists containing the student grades
    for all assignments for the class with id ``class_id``.

    The output of this function is formatted to be used as the
    data source for a Handsontable object. The first row of the
    list contains the names of the assignments. The remainder of
    the rows contain the assignment grades for each student.

    The *rows* are ordered by student id, and the columns are
    ordered by due date.
    """

    query = (class_assignment_query(teacher_id, class_id) &
             (db.classes.id==db.student_classes.class_id) &
             (db.student_classes.student_id==db.student.id) &
             (db.student.user_id==db.auth_user.id) &
             (db.student.id==db.student_grade.student_id) &
             (db.class_grade.grade_id==db.student_grade.grade_id))


    results = db(query).select(db.student_grade.id,
                               db.student.id,
                               db.auth_user.first_name,
                               db.auth_user.last_name,
                               db.grade.name,
                               db.student_grade.student_score,
                               orderby=[db.student.id,
                                        db.grade.due_date])

    assignments = []

    for student in get_class_roster(teacher_id, class_id):
        grades = results.find(lambda s: s.student.id==student[0])
        for grade in grades:
            student.append(grade.student_grade.id)
            student.append(grade.student_grade.student_score)
        assignments.append(student)

    return assignments

def get_standards_for_class(class_id):
    query = ((db.classes.id==class_id) &
             (db.classes.content_area==db.standard.content_area))

    results = db(query).select(db.standard.id, db.standard.short_name,
                               orderby=db.standard.short_name)

    return results


def get_class_total_score(class_id):
    """
    Return a float representing the total of student's grade for given class_id.
    """

    query = ((db.classes.id==class_id) &
             (db.class_grade.class_id==class_id) &
             (db.class_grade.grade_id==db.grade.id) &
             (db.classes.id==db.student_classes.class_id) &
             (db.student_classes.student_id==db.student.id) &
             (db.student.user_id==db.auth_user.id) &
             (db.student.id==db.student_grade.student_id) &
             (db.student_grade.grade_id==db.grade.id) &
             (db.grade.due_date != None ) &
             (db.grade.due_date < datetime.datetime.now()))


    student_point_list = db(query).select(db.student_grade.student_score)
    results = 0.0
    for row in student_point_list:
        results = row.student_score + results

    return results


def get_class_total_possible(class_id):
    """
    Return a float representing the total of possible grade for given class_id.
    """
    query = ((db.classes.id==class_id) &
                 (db.class_grade.class_id==class_id) &
                 (db.class_grade.grade_id==db.grade.id) &
                 (db.classes.id==db.student_classes.class_id) &
                 (db.student_classes.student_id==db.student.id) &
                 (db.student.user_id==db.auth_user.id) &
                 (db.student.id==db.student_grade.student_id) &
                 (db.student_grade.grade_id==db.grade.id) &
                 (db.grade.due_date != None ) &
                 (db.grade.due_date < datetime.datetime.now()))


    max_point_list = db(query).select(db.grade.score)
    results = 0.0
    for row in max_point_list:
        results = row.score + results

    return results

def get_contextual_classes(point):
    """
    Return a string to be use with bootstrap coloring in views."
    """
    if ( point >= 90):
        return 'success'
    elif ( (point >= 80) & (point < 89) ):
        return 'warning'
    else:
        return 'danger'

def get_student_assignment_average(student_id, class_id):
    """
    Return a list containing particular student's total score and total possible score.
    
    When using this function, store the result in a list for the ability to access 
    the score individually.
    To calculate the average, simiply do list[0]/list[1]
    """
    query = ((db.classes.id == class_id) &
             (db.class_grade.class_id == db.classes.id) &
             (db.class_grade.grade_id == db.grade.id) &
             (db.grade.due_date < datetime.datetime.now()) &
             (db.grade.due_date != None) &
             (db.grade.id == db.student_grade.grade_id ) &
             (db.student_grade.student_id == db.student.id ) &
             (db.student.id == student_id))
    grade_list = db(query).select(db.grade.name, db.grade.score, db.student_grade.student_score)

    student_score = 0.0
    possible_score = 0.0
    for row in grade_list:
        student_score = row.student_grade.student_score + student_score
        possible_score = row.grade.score + possible_score

    return ([student_score, possible_score])

def get_student_assignment_due(student_id, class_id):
    """
    Return a :py:class:`Rows <pydal.objects.Rows>` object containing
    all of the assignments for the class with id ``class_id`` 
    and for the student with id ``student_id``, sorted
    by due date.

    Each :py:class:`Row <pydal.objects.Row>` object has the following fields:

    - ``grade.name, grade.score, grade.due_date``
    """
    query = ((db.classes.id == class_id) &
             (db.class_grade.class_id == db.classes.id) &
             (db.class_grade.grade_id == db.grade.id) &
             (db.grade.id == db.student_grade.grade_id ) &
             (db.student_grade.student_id == db.student.id ) &
             (db.student.id == student_id) &
             (db.grade.due_date != None) &
             (db.grade.due_date > datetime.datetime.now()))

    due_list = db(query).select(db.grade.name, db.grade.score, db.grade.due_date,orderby=db.grade.due_date)

    return (due_list)


def get_student_assignment_list(student_id, class_id):
    """
    Return a :py:class:`Rows <pydal.objects.Rows>` object containing
    all of the assignments for the class with id ``class_id``
    and for the student with id ``student_id``, filter by today's date 
    and sorted by due date.

    Each :py:class:`Row <pydal.objects.Row>` object has the following fields:

    - ``grade.name, grade.score, grade.due_date, student_grade.student_score``
    """
    query = ((db.classes.id == class_id) &
             (db.class_grade.class_id == db.classes.id) &
             (db.class_grade.grade_id == db.grade.id) &
             (db.grade.id == db.student_grade.grade_id ) &
             (db.student_grade.student_id == db.student.id ) &
             (db.student.id == student_id) &
             (db.grade.due_date != None))

    assignment_list = db(query).select(db.grade.name, db.grade.score, db.grade.due_date, db.student_grade.student_score, orderby=db.grade.due_date)

    return (assignment_list)

def get_class_name(class_id):
    """
    Return a string containing class's name when giving ``class_id``
    """
    query = ((db.classes.id == class_id))
    name = db(query).select(db.classes.name)
    return(name[0])

def get_student_name(student_id):
    """
    Return a string containing student's name when giving ``student_id``
    """
    query = ((db.student.user_id == student_id) &
             (db.auth_user.id == db.student.user_id))
    name = db(query).select(db.auth_user.first_name, db.auth_user.last_name)
    return (name[0])

################################################
if __name__ == '__main__':
    pass
