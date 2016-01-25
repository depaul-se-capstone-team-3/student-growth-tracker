#Grades/assessments table creation

db.define_table(
    'grade_type',
    Field('name', 'string', required=True),
    Field('description', 'string'))
db.grade_type.id.readable = db.grade_type.id.writable = False

db.define_table(
    'grade',
    Field('name', 'string', required=True, requires=IS_NOT_EMPTY()),
    Field('display_date', 'datetime'),
    Field('date_assigned', 'datetime'),
    Field('due_date', 'datetime'),
    Field('grade_type', 'reference grade_type',
          requires=IS_IN_DB(db, 'grade_type.id', '%(name)s')),
    Field('score', 'double', requires=(IS_FLOAT_IN_RANGE(minimum=0),IS_NOT_EMPTY())),
    #Field('isPassFail', 'boolean', default=False),
    #Field('isPassFail', 'boolean', requires=IS_NOT_EMPTY, default=False),
    format = '%(name)s')
db.grade.id.readable = db.grade.id.writable = False

db.define_table(
    'grade_standard',
    Field('grade_id', 'reference grade'),
    Field('standard_id', 'reference standard'))
db.grade_standard.id.readable = db.grade_standard.id.writable = False

db.define_table(
    'class_grade',
    Field('class_id', 'reference classes'),
    Field('grade_id', 'reference grade'))
db.class_grade.id.readable = db.class_grade.id.writable = False

if __name__ == '__main__':
    pass
