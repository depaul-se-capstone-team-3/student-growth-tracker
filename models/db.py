# -*- coding: utf-8 -*-

db = DAL("sqlite://storage.sqlite")

db.define_table(
    'classes',
    Field('name'),
    Field('gradeLevel', 'integer'),
    Field('startDate', 'integer'),
    Field('endDate', 'integer'),
    # studentList Obj
    Field('studentList'),
    # grade Obj
    Field('grade'),
    # content area Obj
    Field('content_area'),
    format = '%(name)s')

db.classes.name.requires = IS_NOT_EMPTY()
db.classes.gradeLevel.requires = IS_NOT_EMPTY()
db.classes.startDate.requires = IS_NOT_EMPTY()
db.classes.endDate.requires = IS_NOT_EMPTY()
db.classes.id.readable = db.classes.id.writable = False


db.define_table(
    'standards',
    Field('refNum'),
    Field('shortName'),
    Field('description'),
    format = '%(shortName)s')

db.standards.refNum.requires = IS_NOT_EMPTY()
db.standards.shortName.requires = IS_NOT_EMPTY()
db.standards.description.requires = IS_NOT_EMPTY()
