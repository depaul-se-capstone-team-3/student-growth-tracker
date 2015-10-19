# -*- coding: utf-8 -*-

db.define_table(
    'classes',
    #removing "requires=IS_NOT_EMPTY" due to database complications.
    Field('name', required=True),
    Field('gradeLevel', 'integer', required=True),
    Field('startDate', 'integer', required=True),
    Field('endDate', 'integer', required=True),
    # studentList Obj
    #Field('studentList', 'reference student'),
    # grade Obj
    #Field('grade', 'reference grade'),
    # content area Obj
    Field('content_area', 'reference contentarea'),
    format = '%(name)s')

db.classes.id.readable = db.classes.id.writable = False
