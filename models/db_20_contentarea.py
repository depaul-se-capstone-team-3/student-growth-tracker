# -*- coding: utf-8 -*-

db.define_table(
    'contentarea',
    Field('name', required=True, requires=IS_NOT_EMPTY),
    Field('description'),
    format = '%(name)s')
