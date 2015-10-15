#Grades/assessments table creation
db.define_table(
    'grade',
    Field('name', 'string', requires=IS_NOT_EMPTY()),
    Field('sequenceDate', 'integer', requires=IS_NOT_EMPTY()),
    Field('isPassFail', 'boolean', requires=IS_NOT_EMPTY()),
    Field('keywords'),
    Field('dueDate', 'integer', requires=IS_NOT_EMPTY()),
    format = '%(name)s')
db.grade.id.readable = db.grade.id.writable = False
