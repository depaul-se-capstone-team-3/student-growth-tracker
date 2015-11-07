"""
The classes controller.

Everything concerning classes goes here. Sort of. We'll clarify as we go on.
"""

from gluon.contrib.simplejson import dumps, loads

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
    """
    Retrieves grade information for a given ``class_id``
    and returns it as ``json``.
    """
    teacher_id = auth.user_id
    class_id = (request.args(0) != None) and request.args(0, cast=int) or None

    return dumps(get_student_assignments(teacher_id, class_id))

@auth.requires_login()
def save_student_grades():
    """
    Receives ``json`` data via ajax from the ``handsontable`` object
    and saves it back to the database.
    """
    vargs = request.vars

    for k in vargs.keys():
        student_grades = vargs[k]
        grades = [int(s) for s in student_grades[2:]]
        for i in range(0, len(grades), 2):
            grade_id = grades[i]
            score = float(grades[i+1])
            db.student_grade[grade_id] = dict(student_score=score)

    return dict()
