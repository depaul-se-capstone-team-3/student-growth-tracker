# -*- coding: utf-8 -*-
# try something like

def index(): 
    grid = SQLFORM.smartgrid(db.gradebook)
    return dict(grid=grid)
    #return locals()

def create():
    form = SQLFORM(db.gradebook).process(next=URL('index'))
    return dict(form=form)
