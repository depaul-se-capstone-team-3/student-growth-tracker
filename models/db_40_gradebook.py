# -*- coding: utf-8 -*-

db.define_table(
    'gradebook',
    #needs additional validator to check if in DB.
    Field('classes', 'reference classes'))
