# -*- coding: utf-8 -*-

db.define_table(
    'contentarea',
    #requires=IS_NOT_EMPTY removed from name constraints due to bug.
    Field('name', required=True),
    Field('description'),
    format = '%(name)s')

if __name__ == '__main__':
    pass
