# -*- coding: utf-8 -*-
# try something like
from gluon.tools import Auth
auth = Auth(db)

def create():
    if auth.has_membership(3, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))
    '''basic create for student and redirect to index'''
    form = SQLFORM(db.student).process(next=URL('index'))
    return dict(form=form)

@auth.requires_login()
def index():
    if auth.has_membership(3, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))

    class_id = (request.args(0) != None) and request.args(0, cast=int) or None
    student_id = auth.user_id

    name = get_student_name(student_id).first_name + " " + get_student_name(student_id).last_name
    class_name = get_class_name(class_id).name
    #pull student.id, since get_student_assignment_list needs student.id vs. auth.user_id
    user_id_query = (db.student.user_id == auth.user_id)
    user_id_rows = db(user_id_query).select(db.student.id)
    user_id = 0
    for key in user_id_rows:
        user_id = key.id
        
    assignment_query = get_student_assignment_list(user_id, class_id)

    #[name, score, possible_score, precent, due]
    assignment_data = []

    for row in assignment_query:
        precent = float(row.student_grade.student_score / row.grade.score *100)
        is_due = ""
        if (row.grade.due_date > datetime.datetime.now()):
            is_due = "warning"
        else:
            is_due = "success"
        assignment = [row.grade.name, row.student_grade.student_score, row.grade.score, precent, "{:%b %d, %Y}".format(row.grade.due_date), is_due]
        assignment_data.append(assignment)


    return dict(name=name, class_name=class_name, assignment_data=assignment_data)

@auth.requires_login()
def overview():
    if auth.has_membership(3, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))

    student_id = auth.user_id

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
