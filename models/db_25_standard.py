# -*- coding: utf-8 -*-

db.define_table(
    'standard',
    Field('reference_number', required=True),
    Field('short_name', required=True),
    Field('description', required=True),
    Field('content_area', 'reference contentarea'),
    format = '%(shortName)s')

db.standard.id.readable = db.standard.id.writable = False
