# -*- coding: utf-8 -*-
# try something like
#def index(): return dict(message="hello from create.py")

def index():
    standard = SQLFORM.smartgrid(db.standard)
    return locals()


def create():
    form = SQLFORM(db.standard).process(next=URL('index'))
    return dict(form=form)
