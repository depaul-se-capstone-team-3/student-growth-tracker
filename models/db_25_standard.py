# -*- coding: utf-8 -*-

db.define_table(
    'standard',
    Field('reference_number', required=True, requires=IS_NOT_EMPTY),
    Field('short_name', required=True, requires=IS_NOT_EMPTY),
    Field('description', required=True, requires=IS_NOT_EMPTY),
    Field('content_area', 'reference contentarea'),
    format = '%(shortName)s')

db.standard.id.readable = db.standard.id.writable = False
