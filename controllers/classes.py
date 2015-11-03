"""
The classes controller.

Everything concerning classes goes here. Sort of. We'll clarify as we go on.
"""

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
    """

    teacher_id = auth.user_id # Cache the user id of the logged-in teacher
                              # to make it easier to access and recognize.

    class_id = (request.args(0) != None) and request.args(0, cast=int) or None

    # Defnitely using these
    class_list = get_class_list(teacher_id, class_id)
    class_roster = get_class_roster(teacher_id, class_id)
    class_assignments = get_class_assignments(teacher_id, class_id)
    assignments = get_student_assignments(teacher_id, class_id)
    
    return dict(class_list=class_list,
                class_roster=class_roster,
                class_assignments=class_assignments,
                assignments=assignments)
