# -*- coding: utf-8 -*-
# try something like
def index(): return dict()

def teacher_create():
    query = ((db.auth_group.id == 2))
    role_field = Field('Account_Type', requires=IS_IN_DB(db(query), 'auth_group.id', '%(role)s', zero = None))
    form = SQLFORM.factory(db.auth_user, role_field, submit_button='Create Teacher')

    if form.process().accepted:
        id = db.auth_user.insert(**db.auth_user._filter_fields(form.vars))
        db.auth_membership.insert(user_id = id, group_id = 2)

    return dict(form=form)




def student_create():
    query = ((db.auth_group.id == 3))
    role_field = Field('Account_Type', requires=IS_IN_DB(db(query), 'auth_group.id', '%(role)s', zero = None))
    school_id_field = Field("School_ID_Number")
    grade_level_field = Field("Grade_Level")
    home_field = Field("Home_Address")
    parent_email_field = Field("Parent_Email")
    form = SQLFORM.factory(db.auth_user, role_field, school_id_field, grade_level_field, home_field, parent_email_field, submit_button='Create Student')

    if form.process().accepted:
        id = db.auth_user.insert(**db.auth_user._filter_fields(form.vars))
        db.auth_membership.insert(user_id = id, group_id = 3)
        db.student.insert(user_id = id,
                          school_id_number = form.vars.School_ID_Number,
                          grade_level = form.vars.Grade_Level,
                          home_address = form.vars.Home_Address,
                          parent_email = form.vars.Parent_Email)

    return dict(form=form)




def parent_create():
    query = ((db.auth_group.id == 4))
    role_field = Field('Account_Type', requires=IS_IN_DB(db(query), 'auth_group.id', '%(role)s', zero = None))
    form = SQLFORM.factory(db.auth_user, role_field, submit_button='Create Parent')

    if form.process().accepted:
        id = db.auth_user.insert(**db.auth_user._filter_fields(form.vars))
        db.auth_membership.insert(user_id = id, group_id = 4)

    return dict(form=form)




def assign_teacher_to_class():
    teacher_query = ((db.auth_group.id == 2)&
            (db.auth_membership.group_id == db.auth_group.id)&
            (db.auth_membership.user_id == db.auth_user.id))
    teacher_field = Field("Teacher",  requires=IS_IN_DB(db(teacher_query), "auth_user.id", '%(first_name)s'+' ' + '%(last_name)s', zero = None))

    class_query = ((db.classes.id > 0))
    class_field = Field("Class",  requires=IS_IN_DB(db(class_query), "classes.id", '%(name)s', zero = None))

    form = SQLFORM.factory(teacher_field, class_field, submit_button='Assign To Class')

    if form.process().accepted:
        db.gradebook.insert(teacher = form.vars.Teacher, classes = form.vars.Class)

    return dict(form=form)




def assign_student_to_class():
    student_query = ((db.student.id > 0))
    student_field = Field("Student",  requires=IS_IN_DB(db(student_query), "student.id", '%(school_id_number)s', zero = None))

    class_query = ((db.classes.id > 0))
    class_field = Field("Class",  requires=IS_IN_DB(db(class_query), "classes.id", '%(name)s', zero = None))

    form = SQLFORM.factory(student_field, class_field, submit_button='Assign To Class')

    if form.process().accepted:
        db.student_classes.insert(student_id = form.vars.Student, class_id = form.vars.Class)

    return dict(form=form)

def assign_parent_to_student():
    parent_query = ((db.auth_group.id == 4)&
            (db.auth_membership.group_id == db.auth_group.id)&
            (db.auth_membership.user_id == db.auth_user.id))
    parent_field = Field("Parent",  requires=IS_IN_DB(db(parent_query), "auth_user.id", '%(first_name)s'+' ' + '%(last_name)s', zero = None))

    student_query = ((db.student.id > 0))
    student_field = Field("Student",  requires=IS_IN_DB(db(student_query), "student.id", '%(school_id_number)s', zero = None))

    form = SQLFORM.factory(parent_field, student_field, submit_button='Assign To Student')

    if form.process().accepted:
        db.parent_student.insert(parent_id = form.vars.Parent , student_id = form.vars.Student)

    return dict(form=form)
