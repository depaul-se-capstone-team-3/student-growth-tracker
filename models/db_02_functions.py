"""
Put things here that will be used in multiple places.
"""

def teacher_classes_query(teacher_id, class_id=None):
    query = ((db.gradebook.teacher==teacher_id) &
             (db.gradebook.classes==db.classes.id) &
             (db.classes.content_area==db.contentarea.id))

    if class_id:
        query &= (db.gradebook.classes==class_id)

    return query

def get_class_list(teacher_id, class_id):
    query = teacher_classes_query(teacher_id, class_id)
    result = db(query).select(db.classes.id, db.classes.name, db.contentarea.id,
                              db.contentarea.name)
    return result

def get_class_roster(teacher_id, class_id):
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

def get_class_assignments(teacher_id, class_id):
    query = (teacher_classes_query(teacher_id, class_id) &
             (db.classes.id==db.class_grade.class_id) &
             (db.class_grade.grade_id==db.grade.id))

    class_assignments = db(query).select(db.grade.name,
                                         orderby=db.grade.due_date)

    return class_assignments

def get_student_assignments(teacher_id, class_id):
    assignment_query = teacher_classes_query(teacher_id, class_id)
    assignment_query &= (db.classes.id==db.student_classes.class_id)   # Add the students
    assignment_query &= (db.student_classes.student_id==db.student.id) # via the mapping table.
    assignment_query &= (db.student.user_id==db.auth_user.id)          # Get details from auth_user.
    assignment_query &= (db.student.id==db.student_grade.student_id)   # Find the grades for each student
    assignment_query &= (db.student_grade.grade_id==db.grade.id)       # via the mapping table.

    assignment_results = db(assignment_query).select(db.student.id,
                                                     db.auth_user.first_name,
                                                     db.auth_user.last_name,
                                                     db.grade.name,
                                                     db.student_grade.student_score,
                                                     db.student_grade.id,
                                                     orderby=[db.student.id,
                                                              db.grade.due_date])

    anames = ['', '']
    for a in get_class_assignments(teacher_id, class_id):
        anames.append(a.name)

    assignments = [anames]

    for student in get_class_roster(teacher_id, class_id):
        grades = assignment_results.find(lambda s: s.student.id==student[0])
        for grade in grades:
            student.append(grade.student_grade.student_score)
        assignments.append(student)

    return assignments
