# -*- coding: utf-8 -*-
# try something like
@auth.requires_login()
def index():
    """pull up teacher and classes that match current user and return a grid with the result"""
    constraints = db.gradebook.teacher == auth.user.id
    grid = db(constraints).select(join=db.gradebook.on(
        (db.gradebook.teacher==db.auth_user.id) & (db.gradebook.classes==db.classes.id)))
    # response.flash = 'Class List - %(first_name)s' % auth.user
    return dict(grid=grid)

def create():
    """generate form for new gradebook entry, redirect to index"""
    form = SQLFORM(db.gradebook).process(next=URL('index'))
    return dict(form=form)
