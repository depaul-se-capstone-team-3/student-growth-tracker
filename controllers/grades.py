
import datetime
from types import ListType

@auth.requires_login()
def index():
    grid = db().select(db.grade.id, db.grade.name, db.grade.display_date,
                       db.grade.date_assigned, db.grade.due_date,
                       db.grade.grade_type,db.grade.score, db.grade.isPassFail)
    return dict(grid=grid)

@auth.requires(auth.has_membership(role='Teacher'), requires_login=True)
def create():
    # Generating form for creating a new assignment.
    # If there is an argument class id, check to see if
    # db.classes contains that class.
    class_id = (request.args(0) != None) and request.args(0, cast=int) or None
    if not class_id or not db.classes(class_id):
        session.flash = T('Invalid class ID: "%s"' % class_id)
        redirect(URL('default', 'index'))

    teacher_id = auth.user_id

    query = ((db.classes.id==class_id) &
             (db.classes.content_area==db.contentarea.id) &
             (db.standard.content_area==db.contentarea.id))

    # Creating the drop down menu for Standard.
    standards = db(query).select(db.standard.id,
                                 db.standard.short_name,
                                 db.standard.reference_number)

    options = []
    for row in standards:
        text = '%s - %s' % (row.reference_number, row.short_name)
        options.append(OPTION(text, _value=row.id))

    standards_menu = SELECT(options, _name='standards', _multiple='multiple',
                            _class='generic-widget form-control',
                            _id='standards')

    form = SQLFORM(db.grade)
    # Insert the SELECT object at the end of the form.
    form.insert(-1, standards_menu)

    # Processing the form
    if form.validate():
        response.flash = 'New grade created.'

        # If only one item is selected, form.vars.standards is a string.
        # If multiple items are selected, form.vars.standards is a
        # list of strings.
        if type(form.vars.standards) is not ListType:
            selected_standards = [form.vars.standards]
        else:
            selected_standards = form.vars.standards

        grade_id = db.grade.insert(name=form.vars.name,
                                   display_date=form.vars.display_date,
                                   date_assigned=form.vars.date_assigned,
                                   due_date=form.vars.due_date,
                                   grade_type=form.vars.grade_type,
                                   score=form.vars.score)

        db.class_grade.insert(class_id=class_id, grade_id=grade_id)

        for standard_id in selected_standards:
            db.grade_standard.insert(grade_id=grade_id,
                                     standard_id=standard_id)

        for student in get_class_roster(teacher_id, class_id):
            db.student_grade.insert(student_id=student[0],
                                    grade_id=grade_id,
                                    student_score=0)

        redirect(URL('classes', 'index', args=[class_id]))

    return dict(form=form, standards=standards_menu, class_id=class_id)

@auth.requires_login()
def edit():
    """
    Edit a grade.

    This is horribly redundant. We should probably see if we can
    combine it with the ``create`` function.

    And it probably really needs to be refactored.
    """
    if auth.has_membership(2, auth.user_id):
        pass
    else:
        redirect(URL('classes','index'))

    record_id = (request.args(0) is not None) and request.args(0, cast=int) or None

    if not record_id:
        redirect(URL('classes', 'index'))

    class_info = db((db.grade.id==record_id) &
                    (db.grade.id==db.class_grade.grade_id)).select(
                        db.class_grade.class_id,
                        db.grade.name).first()

    class_id = class_info.class_grade.class_id
    grade_name = class_info.grade.name

    selected_standards_rows = db((db.grade.id==record_id) &
                                 (db.grade.id==db.grade_standard.grade_id)).select(
                                     db.grade_standard.standard_id)

    selected_standards = []
    for standard in selected_standards_rows:
        selected_standards.append(standard.standard_id)

    standards_query = ((db.classes.id==class_id) &
                       (db.classes.content_area==db.contentarea.id) &
                       (db.standard.content_area==db.contentarea.id))

    # Creating the drop down menu for Standard.
    standards = db(standards_query).select(db.standard.id,
                                           db.standard.short_name,
                                           db.standard.reference_number)

    options = []
    for row in standards:
        text = '%s - %s' % (row.reference_number, row.short_name)
        options.append(OPTION(text, _value=row.id))

    standards_menu = SELECT(options, _name='standards', _multiple='multiple',
                            _class='generic-widget form-control',
                            _id='standards', value=selected_standards)

    form = SQLFORM(db.grade, record_id)
    # Insert the SELECT object at the end of the form.
    form.insert(-1, standards_menu)

    # Processing the form
    if form.validate():
        # If only one item is selected, form.vars.standards is a string.
        # If multiple items are selected, form.vars.standards is a
        # list of strings.
        if type(form.vars.standards) is not ListType:
            selected_standards = [form.vars.standards]
        else:
            selected_standards = form.vars.standards

        db.grade[record_id] = dict(name=form.vars.name,
                                   display_date=form.vars.display_date,
                                   date_assigned=form.vars.date_assigned,
                                   due_date=form.vars.due_date,
                                   grade_type=form.vars.grade_type,
                                   score=form.vars.score)

        # Delete any old standards maps.
        mapped_standards = db(db.grade_standard.grade_id==record_id).delete()

        for standard_id in selected_standards:
            db.grade_standard.insert(grade_id=record_id,
                                     standard_id=standard_id)

        redirect(URL('classes', 'index', args=[class_id]))

    return dict(form=form, standards=standards_menu, class_id=class_id)
