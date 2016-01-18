# -*- coding: utf-8 -*-
# try something like
def index(): return dict(message="hello from parents.py")

@auth.requires_login()
def overview():
    #need to get a parent_id. We also need a function to collect all students associated with a given parent_id.
    parent_id = auth.user_id
    #query holds list of students associated with the parent_id
    query = parent_student_query(parent_id)
    student_name = []
    students_info=[]
    student_ids =[]
    class_grades=[]
    unfinished_student_ids = db(query).select(db.student.id)
    snames = db(query).select(db.student.user_id)

    for r in unfinished_student_ids:
        student_ids.append(r.id)
    student_standard=[]
    student_classes=[]
    student_standards=[]
    for r in student_ids:
        classes = get_student_classes(r)
        for c in classes:
            student_classes.append(c.name)
            grade = get_student_assignment_average(r,c.id)
            class_grades.append((grade[0]/grade[1])*100)
            student_standard = get_standards_for_class(c.id)
            for s in student_standard:
                student_standards.append(s.reference_number)

    for s in snames:
        s_name = get_student_name(s.user_id)
        student_name.append(s_name.first_name)
        student_name.append(s_name.last_name)
    
        
    return dict(student_name=student_name, student_classes=student_classes, class_grades=class_grades, student_standard=student_standard, student_standards=student_standards
               )
