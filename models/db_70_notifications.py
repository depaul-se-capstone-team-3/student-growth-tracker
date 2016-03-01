# -*- coding: utf-8 -*-
db.define_table(
    'notifications',
    Field('student_id', 'reference student'),
    Field('class_id', 'reference classes'),
    Field('date','datetime', requires = IS_DATE(format=('%B %d, %Y'))),
    Field('warning_text','string', required=True))
