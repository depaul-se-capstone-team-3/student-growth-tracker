# -*- coding: utf-8 -*-

db.define_table(
    'contentarea',
    Field('name', required=True, requires=IS_NOT_EMPTY()),
    #removed reference to standard
    )
