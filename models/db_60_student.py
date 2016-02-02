#Student table creation
db.define_table(
    'student',
    Field('user_id', 'reference auth_user'),
    Field('school_id_number','string', required=True),
    Field('grade_level','integer', required=True),
    Field('home_address','string'),
    Field('parent_email','string'),
    format = '%(user_id)s')
db.classes.id.readable = db.classes.id.writable = False

db.define_table(
    'parent_student',
    Field('parent_id', 'reference auth_user'),
    Field('student_id', 'reference student'))
db.parent_student.parent_id.readable = db.parent_student.parent_id.writable = False
db.parent_student.student_id.readable = db.parent_student.student_id.writable = False
    
    
db.define_table(
    'student_classes',
    Field('student_id', 'reference student'),
    Field('class_id', 'reference classes'))
db.student_classes.student_id.readable = db.student_classes.student_id.writable = False
db.student_classes.class_id.readable = db.student_classes.class_id.writable = False

db.define_table(
    'student_grade',
    Field('student_id', 'reference student'),
    Field('grade_id', 'reference grade'),
    Field('student_score', 'float',requires=(IS_FLOAT_IN_RANGE(0,1000))))
db.student_grade.student_id.readable = db.student_grade.student_id.writable = False
db.student_grade.grade_id.readable = db.student_grade.grade_id.writable = False

db.define_table(
    'attendance',
    Field('student_id', 'reference student'),
    Field('class_id', 'reference classes'),
    Field('attendance_date', 'datetime', requires=(IS_DATE)),
    Field('present', 'boolean', default=False, required=True))

if __name__ == '__main__':
    pass
