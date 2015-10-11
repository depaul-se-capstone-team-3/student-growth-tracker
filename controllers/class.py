# -*- coding: utf-8 -*-
# try something like
#def index(): return dict(message="hello from class.py")


def index():
    class_ = SQLFORM.smartgrid(db.class_)
    return locals()


def create():
    form = SQLFORM(db.class_).process(next=URL('index'))
    return dict(form=form)
