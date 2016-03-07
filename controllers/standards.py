# -*- coding: utf-8 -*-
# try something like
#def index(): return dict(message="hello from create.py")
@auth.requires_login()
def index():
    standard = SQLFORM.smartgrid(db.standard)
    return dict(standard=standard)

@auth.requires_login()
def create():
    form = SQLFORM(db.standard).process(next=URL('index'))
    return dict(form=form)
