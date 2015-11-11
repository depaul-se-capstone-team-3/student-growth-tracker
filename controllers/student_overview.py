# -*- coding: utf-8 -*-
# try something like
def overview():
    student_id = (request.args(0) != None) and request.args(0, cast=int) or None
    #if (student_id == None):
       # redirect(URL("default","index"))

    #{id: [name, average, [due_soon]]}
    overview_data = {}
    due_amount = 3

    #To display student name
    name = get_student_name(student_id).first_name + " " + get_student_name(student_id).last_name

    query = ((db.student.user_id == student_id) &
             (db.student.id == db.student_classes.student_id) &
             (db.student_classes.class_id == db.classes.id))
    classes_query = db(query).select(db.classes.id, db.classes.name)

    classes_list = []
    for row in classes_query:
        classes_list.append([int(row.id), row.name])

    for c in classes_list:
        score = get_student_assignment_average(student_id,c[0])
        due_query = get_student_assignment_due(student_id, c[0])
        due_list = []
        due_count = 0
        for row in due_query:
            if (due_count == due_amount):
                break
            else:
                due_count = due_count + 1
                due_list.append(row)
        overview_data[c[0]] = [c[1], format(score[0]/score[1]*100.0 , '.2f'), due_list]

    return dict(name=name, overview_data=overview_data)
