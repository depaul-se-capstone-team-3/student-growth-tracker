# -*- coding: utf-8 -*-
# try something like

@auth.requires_login()
def index():
    class_query = ((db.gradebook.teacher==auth.user_id) &
                   (db.gradebook.classes==db.classes.id) &
                   (db.classes.content_area==db.contentarea.id))
    class_rows = db(class_query).select()

    class_roster_query = ((db.gradebook.teacher==auth.user_id) &
                          (db.gradebook.classes==db.classes.id) &
                          (db.student_classes.student_id==db.student.id) &
                          (db.student.user_id==db.auth_user.id))
    class_roster = db(class_roster_query).select()
    return dict(rows=class_rows, class_roster=class_roster)


def create():
    form = SQLFORM(db.classes, submit_button='Create',
                   labels = {'gradeLevel': 'Grade Level',
                             'startDate': 'Start Date',
                             'endDate': 'End Date'} ).process(next=URL('index'))
    return dict(form=form)
