# -*- coding: utf-8 -*-
# try something like
#def index(): return dict(message="hello from create.py")

def index():
    standards = db().select(db.standards.id, db.standards.refNum, db.standards.shortName, db.standards.description, orderby=db.standards.refNum)
    return dict(standards=standards)


def create():
    form = SQLFORM(db.standards).process(next=URL('index'))
    return dict(form=form)

def show():
    grid = SQLFORM.grid(db.standards.id)
    return dict(grid=grid)
