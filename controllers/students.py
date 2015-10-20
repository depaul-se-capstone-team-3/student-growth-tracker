# -*- coding: utf-8 -*-
# try something like

def index():
    query = ((db.gradebook.teacher==db.auth_user.id) &
             (db.gradebook.classes==db.classes.id))
    # fields = ()
    rows = db(query).select(db.auth_user.first_name, db.auth_user.last_name)
    return dict(rows=rows)


# def index(): 
#     grid = SQLFORM.smartgrid(db.student)
#     return dict(grid=grid)


def create():
    form = SQLFORM(db.student).process(next=URL('index'))
    return dict(form=form)
