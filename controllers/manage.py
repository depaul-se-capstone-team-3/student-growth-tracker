# -*- coding: utf-8 -*-
# try something like
#def index(): return dict(message="hello from manage_users.py")


#@auth.requires_login()

@auth.requires_login()
def index():
    if auth.has_membership(1, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))

    pass

@auth.requires_login()
def users():
    """Simple form showing a list of users, able to create a user using web2py built in functions"""
    #Basic SQLFORM given two connected tables
    if auth.has_membership(1, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))

    form = SQLFORM.smartgrid(db.auth_user, linked_tables=[db.auth_membership,db.auth_group])
    return dict(form=form)

@auth.requires_login()
def current_user():
    """simple query showing a list of current users"""
    #Basic web2py query
    if auth.has_membership(1, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))

    rows = db().select(db.auth_user.first_name, db.auth_user.last_name, db.auth_membership.user_id, db.auth_group.description, db.auth_user.email, 
            left=[db.auth_membership.on(db.auth_user.id==db.auth_membership.user_id), db.auth_group.on(db.auth_membership.group_id==db.auth_group.id)])
    return dict(rows=rows)
