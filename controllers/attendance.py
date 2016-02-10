"""
The attendance controller.

"""
import datetime

WEEKDAY_ABRV = ['M', 'Tu', 'W', 'Th', 'F']

@auth.requires(auth.has_membership(role='Teacher'), requires_login=True)
def index():
    """
    Attendance information for all of a teacher's classes.
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

    # class_roster = get_class_roster(auth.user_id, class_id)

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

    results = db(attendance_query).select(db.student.id,
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
    
    for a in results:
        student_id = a.student.id
        attendance_date = a.attendance.attendance_date
        present = a.attendance.present

        if not raw_attendance.has_key(student_id):
            raw_attendance[student_id] = {}

        raw_attendance[student_id][attendance_date] = present

    days = sorted(class_days.keys())
    
    attendance = {}
    for a in raw_attendance.keys():
        attendance[a] = []
        for i in range(len(days)):
            # attendance[a].append(days[i])
            attendance[a].append(raw_attendance[a].get(days[i], False))

    return dict(date_header=date_header,
                class_list=class_list,
                class_days=class_days,
                attendance=attendance)

def first_weekday_of_month(year, month):
    first = datetime.date(year, month, 1)
    if first.weekday() > 4:
        delta = 7 - first.weekday() % 7
        first = first + datetime.timedelta(delta)
    return first

def last_weekday_of_month(year, month):
    last = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)
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
