# -*- coding: utf-8 -*-

db.define_table(
    'gradebook',
    Field('teacher', 'reference auth_user'),
    Field('classes', 'reference classes'))

if __name__ == '__main__':
    pass
