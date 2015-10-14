# -*- coding: utf-8 -*-

define_table(
    'school'
    Field('name', 'string', required=True, requires=IS_NOT_EMPTY),
    Field('address', 'string' required=True, requires=IS_NOT_EMPTY),
    Field('city', 'string', required=True, requires=IS_NOT_EMPTY),
    Field('state', 'string', required=True, requires=IS_NOT_EMPTY),
    Field('telephone', 'string', requires=IS_EMTPY_OR(IS_PHONE_NUMBER)),
    Field('fax', 'string', requires=IS_EMTPY_OR(IS_PHONE_NUMBER)),
    Field('email', 'string', requires=IS_EMPTY_OR(IS_EMAIL))
)
db.school.id.readable = db.school.id.writable = False

define_table(
    'school_member',
    Field('school_id', 'references school'),
    Field('member_id', 'references auth_user')
)
