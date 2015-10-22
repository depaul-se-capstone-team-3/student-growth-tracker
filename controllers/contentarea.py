# -*- coding: utf-8 -*-
# try something like
def index():
    """basic index, return grid based on available contentareas"""
    grid = SQLFORM.smartgrid(db.contentarea)
    return locals()

def create():
    """basic create, makes form for new contentarea and redirect to index"""
    form = SQLFORM(db.contentarea).process(next=URL('index'))
    return dict(form=form)
