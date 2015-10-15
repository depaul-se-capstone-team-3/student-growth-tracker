#Student table creation
db.define_table(
    'student',
    Field('firstName','string', requires=IS_NOT_EMPTY()),
    Field('lastName','string', requires=IS_NOT_EMPTY()),
    #Field('ID','string', requires=IS_NOT_EMPTY()),
   # Field('studentGrade','int', requires=IS_NOT_EMPTY()),
    Field('schoolName','string', requires=IS_NOT_EMPTY()),
    Field('homeAddress','string', requires=IS_NOT_EMPTY()),
    Field('emailAddress','string', requires=IS_NOT_EMPTY()),
    Field('middleInitial','string'),
    format = '%(ID)s')
db.student.id.readable = db.student.id.writable = False
