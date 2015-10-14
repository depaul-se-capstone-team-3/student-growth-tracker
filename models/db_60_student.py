#Student table creation
db.define_table(
    'student',
    Field('firstName','string', requires=IS_NOT_EMPTY()),
    Field('lastName','string', requires=IS_NOT_EMPTY()),
    Field('ID','string', requires=IS_NOT_EMPTY()),
    Field('studentGrade','int', requires=IS_NOT_EMPTY()),
    Field('schoolName','string', requires=IS_NOT_EMPTY()),
    Field('homeAddress','string', requires=IS_NOT_EMPTY()),
    Field('emailAddress','string', requires=IS_NOT_EMPTY()),
    Field('middleInitial','string'),
    format = '%(ID)s')
db.classes.id.readable = db.classes.id.writable = False

db.define_table(
    'student_classes',
    Field('student_id', 'reference student'),
    Field('class_id', 'reference classes'))
db.student_classes.student_id.readable = db.student_classes.student_id.writable = False
db.student_classes.class_id.readable = db.student_classes.class_id.writable = False
