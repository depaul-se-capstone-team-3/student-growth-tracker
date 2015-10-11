# -*- coding: utf-8 -*-
# try something like
#def index(): return dict(message="hello from create.py")

def index():
    classes = db().select(db.classes.id, db.classes.name, orderby=db.classes.name)
    return dict(classes=classes)


def create():
    form = SQLFORM(db.classes).process(next=URL('index'))
    return dict(form=form)

def show():
    grid = SQLFORM.grid(db.classes.id)
    return dict(grid=grid)

def edit():
    this_class = db.classes(request.args(0,cast=int)) or redirect(URL('index'))
    form = SQLFORM(db.classes, this_class).process(next= URL('show', args=request.args))
    return dict(form=form)
