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
    # Get the list of assignments for each student in the class.
    # Is there a way to do this in one query, which I then break up into a set
    # of dictionaries?
    # Or is it just easier to make objects that know how to deal with these items
    # themselves?

    class_query = ((db.gradebook.teacher==auth.user_id) &
                   (db.gradebook.classes==db.classes.id) &
                   (db.classes.content_area==db.contentarea.id))
    class_rows = db(class_query).select()


    class_roster_query = ((db.gradebook.teacher==auth.user_id) &
                          (db.gradebook.classes==db.classes.id) &
                          (db.student_classes.student_id==db.student.id) &
                          (db.student.user_id==db.auth_user.id))
    class_roster = db(class_roster_query).select(left=db.student_grade.on(db.student.id==db.student_grade.student_id))
    return dict(rows=class_rows, class_roster=class_roster)


# def create():
#     form = SQLFORM(db.classes, submit_button='Create',
#                    labels = {'gradeLevel': 'Grade Level',
#                              'startDate': 'Start Date',
#                              'endDate': 'End Date'} ).process(next=URL('index'))
#     return dict(form=form)
