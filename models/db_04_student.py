# -*- coding: utf-8 -*-
class Student:
    'A class that is a reference to an individual student at a school.'

    def __init__(self, id, fname,lname,uName, passw, specials, gLevel, schoolN, hAddress, pEmail, cGrade):
        self.ID = id
        self.firstName = fname
        self.lastName = lname
        self.userName = uName
        self.password = passw
        self.specialServices = specials
        self.gradeLevel = gLevel
        self.school = schooln
        self.homeAddress = hAddress
        self.parentEmail = pEmail
        self.currentGrade = cGrade
b.define_table(
    'student',
    Field('id', 'integer', requires=IS_NOT_EMPTY()),
    Field('firstName', 'string', requires=IS_NOT_EMPTY()),
    Field('lastName', 'string', requires=IS_NOT_EMPTY()),
    Field('userName', 'string', requires=IS_NOT_EMPTY()),
    Field('password', 'string', requires=IS_NOT_EMPTY()),
    Field('specialServices'),
    Field('gradeLevel', 'integer', requires=IS_NOT_EMPTY()),
    Field('school', 'string', requires=IS_NOT_EMPTY()),
    Field('homeAddress', 'string', requires=IS_NOT_EMPTY()),
    Field('parentEmail', 'string'),
    Field('currentGrade', 'string', requires=IS_NOT_EMPTY()),
    format = '%(id)s')

db.class_.id.readable = db.class_.id.writable = False
