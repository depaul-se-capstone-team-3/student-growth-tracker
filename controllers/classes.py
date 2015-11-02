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

    teacher_id = auth.user_id # Cache the user id of the logged-in teacher
                              # to make it easier to access and recognize.

    # Check if we were passed a class id. If so, it's stored in ``class_id``.
    # If not, ``class_id`` gets ``None``.
    # I'm using a common Python idiom here.
    # Note to self: Find the link to the explanation and add it here.
    class_id = (request.args(0) != None) and request.args(0, cast=int) or None

    # Create a ``Query`` object that represents the set of classes
    # associated with the teacher currently logged in.
    # The ``teacher_classes`` Query object is never used directly to query
    # the database. It is used as the base upon which other queries are built.
    teachers_classes = ((db.gradebook.teacher==teacher_id) &
                        (db.gradebook.classes==db.classes.id))

    # If we were given a class id, update the query to
    # only include that class.
    if class_id:
        teachers_classes &= db.gradebook.classes==class_id

    # To display the name of the content area for the class,
    # we need to add the information from the ``db.contentarea`` table.
    class_query = (teachers_classes &
                   (db.classes.content_area==db.contentarea.id))

    # We use the ``class_query`` Query object to get the ``Set``
    # of records we'll display in the view.
    class_list = db(class_query).select(db.classes.id, db.classes.name,
                                        db.contentarea.id, db.contentarea.name)

    # To get the list of students in the class, we need to add
    # information from the student tables. We start with the
    # ``teachers_classes`` query, which restricts the students
    # to the members of the class.
    class_roster_query = (teachers_classes &
                          (db.classes.id==db.student_classes.class_id) &
                          (db.student_classes.student_id==db.student.id) &
                          (db.student.user_id==db.auth_user.id))

    # ``class_roster`` now holds the ``Set`` of students in the class.
    # An empty select returns all fields from all tables in the query.
    # By listing just the fields I want in the ``select`` method,
    # I can restrict the information returned in the ``Set`` to
    # only what I need.
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

    # This gets the list of assignments for this class. It's only used to
    # generate the header row.
    # 
    # To ensure that the headers and student grades match up, we use
    # ``orderby`` on the same field in both queries to sort the results.
    class_assignments_query = (class_query &
                               (db.classes.id==db.class_grade.class_id) &
                               (db.class_grade.grade_id==db.grade.id))
    class_assignments = db(class_assignments_query).select(db.grade.name,
                                                           orderby=db.grade.due_date)

    # assignment_query = (db.gradebook.teacher==teacher_id)
    # assignment_query &= (db.gradebook.classes==db.classes.id)

    # if class_id:
    #     assignment_query &= (db.classes.id==class_id)

    # We start with ``class_query``.
    assignment_query = class_query
    assignment_query &= (db.classes.id==db.student_classes.class_id)   # Add the students
    assignment_query &= (db.student_classes.student_id==db.student.id) # via the mapping table.
    assignment_query &= (db.student.user_id==db.auth_user.id)          # Get details from auth_user.
    assignment_query &= (db.student.id==db.student_grade.student_id)   # Find the grades for each student
    assignment_query &= (db.student_grade.grade_id==db.grade.id)       # via the mapping table.

    # Run the query as usual.
    # Again, we're restricting the results to just the fields we need
    # to cut down on overhead. We also sort the results in the same order
    # as the headers so everything lines up nicely.
    assignment_results = db(assignment_query).select(db.student.id,
                                                     db.grade.name,
                                                     db.student_grade.student_score,
                                                     db.student_grade.id,
                                                     orderby=db.grade.due_date)

    # This will need to be made more robust once we account for
    # missing entries in the tables.

    # The ``Set`` ``assignment_results`` now holds the grades for each student.
    # Unfortunately, we have rows of assignments. We want the assignments
    # to be the columns of our table, so we have to "pivot" everything around
    # ``student.id``.

    # We start by creating an empty dictionary. We'll use ``student.id``
    # as the key to make it easy to retrieve the list of grades we want.
    # In this case, the list is an actual Python list that we build up as we
    # go through the result set.
    assignments = {}

    # Now we loop over the ``Set`` of rows.
    for a in assignment_results:
        # Check if we've already added this ``student.id`` to the dictionary.
        # If so, we just append another score to the list.
        if a.student.id in assignments:
            #declare a tuple of student_score and id to faciliate editing grades
            b = (a.student_grade.student_score, a.student_grade.id)
            #pass tuple into assignments list
            assignments[a.student.id].append(b)
            #assignments[a.student.id].append(a.student_grade.student_score, a.student_grade.id)
        # If not, we need to initialize the list of grades for this
        # ``student.id``.
        # See the Python documentation on ``dict`` and ``list`` to see
        # the details on why this particular syntax works.
        else:
            #Placeholder for errors.  We will need to update eventually.
            assignments[a.student.id] = [(a.student_grade.student_score, a.student_grade.id)]

    # Now we send all of the parts to the view. The logic in the view will
    # lay evrything out the way we want.
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
