# -*- coding: utf-8 -*-
# try something like
#def index(): return dict(message="hello from manage_users.py")


#@auth.requires_login()


def index():
    form = SQLFORM.smartgrid(db.auth_user, linked_tables=[db.auth_membership,db.auth_group])
    return dict(form=form)

def current_user():
    rows = db().select(db.auth_user.first_name, db.auth_user.last_name, db.auth_membership.user_id, db.auth_group.description, db.auth_user.email, 
            left=[db.auth_membership.on(db.auth_user.id==db.auth_membership.user_id), db.auth_group.on(db.auth_membership.group_id==db.auth_group.id)])
    return dict(rows=rows)

'''

def test():
    query = (db.auth_user.id > 0)
    t1 = (db.auth_user.id==db.auth_membership.user_id)
    rows = db(query).select(db.auth_user.first_name, db.auth_user.last_name, db.auth_user.username, db.auth_membership.group_id, left=db.auth_membership.on(t1))
    return dict(rows=rows)

def test2():
    form = SQLFORM(db.auth_user, deletable=True, fields=None, delete_label='Check to delete:', submit_button='Create', showid=True)
    extra = TR(LABEL("Account Type"), INPUT(_name='nam'))
    form[0].insert(-1,extra)
    if form.process().accepted:
        response.flash = "form accepted"
    elif form.errors:
        response.flash = "form has errors"
    else:
        response.flash = "please fill out the form"
    return dict(form=form)

def test3():
    query = (db.auth_group.role == 'Student')
    db.auth_group.role.requires=IS_IN_DB(db, 'auth_group.role', '%(role)s', zero=T('Choose Type'))
    form = SQLFORM.factory(db.auth_user, db.auth_group, fields=['first_name', 'last_name', 'email', 'username', 'password', 'role'], submit_button='Create', labels = {'role': 'Account Type'})
    if form.process().accepted:
        id = db.auth_user.insert(**db.auth_user._filter_fields(form.vars))
        form.vars.auth_user=id
        id = db.auth_membership.insert(**db.auth_membership._filter_fields(form.vars))

        #input_username = db.auth_user._filter_fields(form.vars)['username']
        #input_role = db.auth_group._filter_fields(form.vars)['role']

        response.flash = "New account created"
    return dict(form=form)

'''
