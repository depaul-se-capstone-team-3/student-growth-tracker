"""A script for loading dummy data into the database. Manual loading is hard."""

import os.path

data_path_pattern = os.path.join(request.folder, 'private', 'dummy_files/load_%02d_db_%s_dummy.csv')
path = None

try:
    if db(db.contentarea).isempty():
        path = data_path_pattern % (20, 'contentarea')
        db.contentarea.import_from_csv_file(open(path, 'r'))

    if db(db.standard).isempty():
        path = data_path_pattern % (25, 'standard')
        db.standard.import_from_csv_file(open(path, 'r'))

    if db(db.classes).isempty():
        path = data_path_pattern % (30, 'classes')
        db.classes.import_from_csv_file(open(path, 'r'))

    if db(db.gradebook).isempty():
        path = data_path_pattern % (40, 'gradebook')
        db.gradebook.import_from_csv_file(open(path, 'r'))

    if db(db.grade).isempty():
        path = data_path_pattern % (50, 'grade')
        db.grade.import_from_csv_file(open(path, 'r'))

    if db(db.grade_standard).isempty():
        path = data_path_pattern % (51, 'grade_standard')
        db.grade_standard.import_from_csv_file(open(path, 'r'))

    if db(db.class_grade).isempty():
        path = data_path_pattern % (52, 'class_grade')
        db.class_grade.import_from_csv_file(open(path, 'r'))

    if db(db.student).isempty():
        path = data_path_pattern % (60, 'student')
        db.student.import_from_csv_file(open(path, 'r'))

    if db(db.student_classes).isempty():
        path = data_path_pattern % (61, 'student_classes')
        db.student_classes.import_from_csv_file(open(path, 'r'))

except Exception, e:
    response.flash = '%s: loading %s' % (e, path)

data_path_pattern = None
