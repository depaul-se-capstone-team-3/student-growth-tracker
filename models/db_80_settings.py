# -*- coding: utf-8 -*-
db.define_table(
    'settings',
    Field('location', 'string', notnull=True),
    Field('setting','float', required=True))
