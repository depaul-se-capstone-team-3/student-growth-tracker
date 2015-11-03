"""
Put things here that will be used in multiple places.
"""

def teacher_classes_query(teacher_id, class_id=None):
    """Return a :mod:`Query` object that defines the set of classes associated with
    ``teacher_id. If ``class_id`` is provided, return only that class. This may
    seem redunant, but it provides an easy way to ensure that the query returns
    only those classes associated with ``teacher_id``."""
    query = ((db.gradebook.teacher==teacher_id) &
             (db.gradebook.classes==db.classes.id))

    if class_id:
        query &= (db.gradebook.classes==class_id)

    return query

def class_query(teacher_id, class_id=None):
    """To display the name of the content area for the class,
    we need to add the information from the ``db.contentarea`` table."""
    query = (teacher_classes_query(teacher_id, class_id) &
             (db.classes.content_area==db.contentarea.id))

    return query

def get_class_list(teacher_id, class_id):
    """We use the ``cq`` Query object to get the ``Set``
    of records we'll display in the view."""
    result = db(class_query(teacher_id, class_id)).select(db.classes.id,
                                                          db.classes.name,
                                                          db.contentarea.id,
                                                          db.contentarea.name)
    return result

def class_roster_query(teacher_id, class_id):
    """To get the list of students in the class, we need to add
    information from the student tables. We start with the
    ``tcq`` query, which restricts the students
    to the members of the class."""
    query = (teacher_classes_query(teacher_id, class_id) &
             (db.classes.id==db.student_classes.class_id) &
             (db.student_classes.student_id==db.student.id) &
             (db.student.user_id==db.auth_user.id))
    return query

def get_class_roster(teacher_id, class_id):
    results = db(class_roster_query(teacher_id, class_id)).select(db.student.id,
                                                                  db.auth_user.first_name,
                                                                  db.auth_user.last_name)
    return results
