# -*- coding: utf-8 -*-
# try something like
def index(): 
    grid = SQLFORM.smartgrid(db.student)
    return dict(grid=grid)

def create():
    form = SQLFORM(db.student).process(next=URL('index'))
    return dict(form=form)
