# -*- coding: utf-8 -*-
# try something like
@auth.requires_login()
#def index():
#    query = db.gradebook.teacher == auth.user_id
#    gradebook = db(query)
#    return dict(message='Class List - %(first_name)s' % auth.user,gradebook=gradebook)
def index():
    constraints = db.gradebook.teacher == auth.user.id
    grid = SQLFORM.smartgrid(db.gradebook,constraints={'gradebook':(db.gradebook.teacher==auth.user_id)},links_in_grid=False)
    return dict(message='Class List - %(first_name)s' % auth.user,grid=grid)

def create():
    form = SQLFORM(db.gradebook).process(next=URL('index'))
    return dict(message='Add Class to %(first_name)s Gradebook' % auth.user,form=form)
