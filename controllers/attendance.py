"""
The attendance controller.

"""
import datetime

from gluon.contrib.simplejson import dumps, loads

WEEKDAY_ABRV = ['M', 'Tu', 'W', 'Th', 'F']

@auth.requires(auth.has_membership(role='Teacher'), requires_login=True)
def index():
    """
    Attendance information for all of a teacher's classes.

    Something we might want to add:
    Save the class ID and date into a session variable.
    If the class ID changes, use the saved date.

    Also, maybe the mobile view only shows 5 days. Or 10?
    """

    class_id = (request.args(0) is not None) and request.args(0, cast=int) or None

    if not class_id:
        response.flash = T("Class Does Not Exist")
        session.flash = T("Class does not exist.")

        # Redirect to previous link if via link, else redirect to main page.
        if (request.env.http_referer==None):
            redirect(URL('default', 'index'))
        else:
            redirect(request.env.http_referer)

    year = (request.args(1) is not None) and request.args(1, cast=int) or datetime.date.today().year
    month = (request.args(2) is not None) and request.args(2, cast=int) or datetime.date.today().month

    month_begin_date = first_weekday_of_month(year, month)
    month_end_date = last_weekday_of_month(year, month)
    class_days = class_days_this_month(month_begin_date, month_end_date)

    date_header = month_begin_date.strftime('%B, %Y')

    student_query = teacher_classes_query(auth.user_id)
    student_query &= ((db.student_classes.class_id==class_id) &
                      (db.student_classes.class_id==db.classes.id) &
                      (db.student.id==db.student_classes.student_id) &
                      (db.auth_user.id==db.student.user_id))

    class_list_set = db(student_query).select(db.student.id,
                                              db.auth_user.last_name,
                                              db.auth_user.first_name,
                                              orderby=[db.auth_user.last_name,
                                                       db.auth_user.first_name])

    class_list = {}
    for s in class_list_set:
        class_list[s.auth_user.last_name + ', ' + s.auth_user.first_name] = s.student.id

    attendance_query = teacher_classes_query(auth.user_id)
    attendance_query &= ((db.student_classes.class_id==class_id) &
                         (db.student_classes.class_id==db.classes.id) &
                         (db.student.id==db.student_classes.student_id))

    results = db(attendance_query).select(db.attendance.id,
                                          db.student.id,
                                          db.attendance.attendance_date,
                                          db.attendance.present,
                                          orderby=db.attendance.attendance_date,
                                          left=db.attendance.on(
                                              (db.attendance.class_id==class_id) &
                                              (db.attendance.class_id==db.classes.id) &
                                              (db.attendance.student_id==db.student.id) &
                                              (db.attendance.attendance_date>=month_begin_date) &
                                              (db.attendance.attendance_date<=month_end_date)))

    raw_attendance = {}

    for student_attendance_info in results:
        attendance_record_id = student_attendance_info.attendance.id
        student_id = student_attendance_info.student.id
        attendance_date = student_attendance_info.attendance.attendance_date
        present = student_attendance_info.attendance.present

        if not raw_attendance.has_key(student_id):
            raw_attendance[student_id] = {}

        raw_attendance[student_id][attendance_date] = (attendance_record_id, present)

    ordered_class_day_list = sorted(class_days.keys())

    attendance = {}
    for student_id in raw_attendance.keys():
        attendance[student_id] = {}
        for class_day in ordered_class_day_list:
            attendance[student_id][class_day] = raw_attendance[student_id].get(class_day, ('N/A', False))

    return dict(class_id=class_id,
                date_header=date_header,
                menu_months=months_in_session(),
                class_list=class_list,
                class_days=class_days,
                attendance=attendance)

def save_attendance_info():
    """
    Receives ``json`` data via ajax from the attendance table and
    saves it back to the database.
    """

    attendance_id = request.vars.attendance_id
    class_day = datetime.datetime.strptime(request.vars.class_day, '%Y-%m-%d')
    student_id = int(request.vars.student_id)
    class_id = int(request.vars.class_id)
    is_present = request.vars.present == 'true'
    new_id = None

    if attendance_id != 'N/A':
        db.attendance[int(attendance_id)] = dict(present=is_present)
    else:
        new_id = db.attendance.insert(student_id=student_id,
                                      class_id=class_id,
                                      attendance_date=class_day,
                                      present=is_present)

    return dumps(dict(new_id=new_id))

def first_weekday_of_month(year, month):
    first = datetime.date(year, month, 1)
    if first.weekday() > 4:
        delta = 7 - first.weekday() % 7
        first = first + datetime.timedelta(delta)
    return first

def last_weekday_of_month(year, month):
    month_part = (month % 12) + 1
    year_part = year + (month / 12)
    last = datetime.date(year_part, month_part, 1) - datetime.timedelta(days=1)
    if last.weekday() > 4:
        delta = 3 - (7 - last.weekday() % 7)
        last = last - datetime.timedelta(delta)
    return last

def class_days_this_month(first_day, last_day):
    snp_days = db((db.students_not_present.date>=first_day) &
                  (db.students_not_present.date<=last_day)).select(db.students_not_present.date,
                                                                   db.students_not_present.title,
                                                                   orderby=db.students_not_present.date)
    non_attendance = {}
    for row in snp_days:
        non_attendance[row.date] = row.title

    dates = {}
    current = first_day
    while current <= last_day:
        wkdy = current.weekday()
        if wkdy < 5:
            dates[current] = (WEEKDAY_ABRV[wkdy], non_attendance.get(current))
        current = current + datetime.timedelta(days=1)

    return dates

def months_in_session():
    first_day = db.students_not_present.date.min()
    open_date = db().select(first_day).first()[first_day]

    last_day = db.students_not_present.date.max()
    close_date = db().select(last_day).first()[last_day]

    months = []
    current = open_date

    while current < close_date:
        months.append((current.strftime('%Y/%m'), current.strftime('%B, %Y')))
        new_month = (current.month % 12) + 1
        new_year = current.year + (current.month / 12)
        current = current.replace(year=new_year, month=new_month)

    return months
