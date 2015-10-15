# -*- coding: utf-8 -*-

db.define_table(
    'standard',
    Field('refNum', required=True, requires=IS_NOT_EMPTY),
    Field('shortName', required=True, requires=IS_NOT_EMPTY),
    Field('description', required=True, requires=IS_NOT_EMPTY),
    format = '%(shortName)s')

db.standard.id.readable = db.standard.id.writable = False
