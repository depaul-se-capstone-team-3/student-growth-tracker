# -*- coding: utf-8 -*-

db.define_table(
    'standard',
    Field('reference_number', required=True),
    Field('short_name', required=True),
    Field('description', required=True),
    Field('content_area', 'reference contentarea'),
    Field('grade_level', required=True),
    format = '%(short_name)s')

db.standard.id.readable = db.standard.id.writable = False

if __name__ == '__main__':
    pass
