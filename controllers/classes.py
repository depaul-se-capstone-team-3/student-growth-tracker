# -*- coding: utf-8 -*-
# try something like

@auth.requires_login()
def index():
    query = ((db.gradebook.teacher==auth.user_id) &
             (db.gradebook.classes==db.classes.id) &
             (db.classes.content_area==db.contentarea.id)
    )
    rows = db(query).select()#db.auth_user.first_name,
                            # db.auth_user.last_name,
                            # db.classes.name,
                            # db.contentarea.name)
    return dict(rows=rows)


def create():
    form = SQLFORM(db.classes, submit_button='Create', labels = {'gradeLevel': 'Grade Level', 'startDate': 'Start Date', 'endDate': 'End Date'} ).process(next=URL('index'))
    return dict(form=form)
