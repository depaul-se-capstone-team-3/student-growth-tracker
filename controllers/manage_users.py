# -*- coding: utf-8 -*-
# try something like
#def index(): return dict(message="hello from manage_users.py")


#@auth.requires_login()


def index():
    '''simple form showing a list of users, able to create a user using web2py built in functions'''
    #Basic SQLFORM given two connected tables
    form = SQLFORM.smartgrid(db.auth_user, linked_tables=[db.auth_membership,db.auth_group])
    return dict(form=form)

def current_user():
    '''simple query showing a list of current users'''
    #Basic web2py query
    rows = db().select(db.auth_user.first_name, db.auth_user.last_name, db.auth_membership.user_id, db.auth_group.description, db.auth_user.email, 
            left=[db.auth_membership.on(db.auth_user.id==db.auth_membership.user_id), db.auth_group.on(db.auth_membership.group_id==db.auth_group.id)])
    return dict(rows=rows)
