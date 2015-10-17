# -*- coding: utf-8 -*-
# try something like
def index(): 
    grid = SQLFORM.smartgrid(db.grade)
    return dict(grid=grid)

def create():
    form = SQLFORM(db.grade).process(next=URL('index'))
    return dict(form=form)
