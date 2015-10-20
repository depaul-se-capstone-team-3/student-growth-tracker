# -*- coding: utf-8 -*-
# try something like
@auth.requires_login()
#def index():
#    query = db.gradebook.teacher == auth.user_id
#    gradebook = db(query)
#    return dict(message='Class List - %(first_name)s' % auth.user,gradebook=gradebook)
@auth.requires_login()
def index():
    constraints = db.gradebook.teacher == auth.user.id
    # grid = SQLFORM(db.gradebook).process()
    grid = db(db.gradebook.teacher).select(join=db.gradebook.on((db.gradebook.teacher==db.auth_user.id) &
                                                                (db.gradebook.classes==db.classes.id)))
    # grid = SQLFORM.smartgrid(db.gradebook,constraints={'gradebook':(db.gradebook.teacher==auth.user_id)})
    # response.flash = 'Class List - %(first_name)s' % auth.user
    return dict(grid=grid)

def create():
    form = SQLFORM(db.gradebook).process(next=URL('index'))
    return dict(form=form)
