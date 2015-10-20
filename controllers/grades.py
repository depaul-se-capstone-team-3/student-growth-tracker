# -*- coding: utf-8 -*-
# try something like
def index(): 
    grid = SQLFORM.smartgrid(db.grade)
    return dict(grid=grid)

def create():
    form = SQLFORM(db.grade).process(next=URL('index'))
    return dict(form=form)

def class_grades():
    query = (db.grade.id==db.class_grade.grade_id) & (db.class_grade.class_id==db.classes.id)
    rows = db(query).select()
    return dict(rows=rows)
