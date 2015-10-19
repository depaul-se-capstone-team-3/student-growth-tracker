# -*- coding: utf-8 -*-
# try something like
def index():
    grid = SQLFORM.smartgrid(db.contentarea)
    return locals()

def create():
    form = SQLFORM(db.contentarea).process(next=URL('index'))
    return dict(form=form)
