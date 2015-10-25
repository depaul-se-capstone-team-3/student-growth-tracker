# -*- coding: utf-8 -*-
# try something like

@auth.requires_login()
def index():
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

    .. todo:: Move the queries into either the ``db_01_general.py`` script, or
              the ``db_30_classes.py`` script.
    """

    # Get the list of classes.
    # Get the list of students in each class
    # Get the list of assignments for the class.
    # Get the list of assignments for each student in the class.

    teacher_id = auth.user_id
    class_id = (request.args(0) != None) and request.args(0, cast=int) or None

    teachers_classes = ((db.gradebook.teacher==auth.user_id) &
                        (db.gradebook.classes==db.classes.id))

    if class_id:
        teachers_classes &= db.gradebook.classes==class_id

    class_query = (teachers_classes &
                   (db.classes.content_area==db.contentarea.id))
    class_list = db(class_query).select()
    
    class_roster_query = (teachers_classes &
                          (db.classes.id==db.student_classes.class_id) &
                          (db.student_classes.student_id==db.student.id) &
                          (db.student.user_id==db.auth_user.id))
    class_roster = db(class_roster_query).select(db.student.id,
                                                 db.auth_user.first_name,
                                                 db.auth_user.last_name)

    # I think this whole thing can be simplified.
    # Once it's working, I'll try to do that.
    # At a minimum, this will need to be converted to using a left outer join
    # to account for missing assignments and things like that.
    # This is very much a first draft.

    # I'm leaving these here temporarily because I think I might need to use
    # something like this for the left outer joins.
    # sg1 = db.student_grade.with_alias('sg1')
    # sg2 = db.student_grade.with_alias('sg2')
    class_assignments_query = (class_query &
                               (db.classes.id==db.class_grade.class_id) &
                               (db.class_grade.grade_id==db.grade.id))
    class_assignments = db(class_assignments_query).select(db.grade.name,
                                                           orderby=db.grade.due_date)
    assignment_query = (db.gradebook.teacher==teacher_id)
    assignment_query &= (db.gradebook.classes==db.classes.id)

    if class_id:
        assignment_query &= (db.classes.id==class_id)

    assignment_query &= (db.classes.id==db.student_classes.class_id)
    assignment_query &= (db.student_classes.student_id==db.student.id)
    assignment_query &= (db.student.user_id==db.auth_user.id)
    assignment_query &= (db.student.id==db.student_grade.student_id)
    assignment_query &= (db.student_grade.grade_id==db.grade.id)

    assignment_results = db(assignment_query).select(db.student.id,
                                                     db.grade.name,
                                                     db.student_grade.student_score,
                                                     orderby=db.grade.due_date)

    # This will need to be made more robust once we account for
    # missing entries in the tables.
    assignments = {}
    for a in assignment_results:
        if a.student.id in assignments:
            assignments[a.student.id].append(a.student_grade.student_score)
        else:
            assignments[a.student.id] = [a.student_grade.student_score]

    return dict(class_list=class_list,
                class_roster=class_roster,
                class_assignments=class_assignments,
                assignments=assignments)

# @auth.requires_login()
# def create():
#     form = SQLFORM(db.classes, submit_button='Create',
#                    labels = {'gradeLevel': 'Grade Level',
#                              'startDate': 'Start Date',
#                              'endDate': 'End Date'} ).process(next=URL('index'))
#     return dict(form=form)
