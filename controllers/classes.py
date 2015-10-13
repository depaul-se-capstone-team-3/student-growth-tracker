# -*- coding: utf-8 -*-
# try something like

def index():
    classes = SQLFORM.smartgrid(db.classes)
    return locals()


def create():
    form = SQLFORM(db.classes).process(next=URL('index'))
    return dict(form=form)
