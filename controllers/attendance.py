"""
The attendance controller.

"""
import datetime

@auth.requires(auth.has_membership(role='Teacher'), requires_login=True)
def index():
    """
    Attendance information for all of a teacher's classes.
    """
    year = (request.args(0) is not None) and \
           request.args(0, cast=int) or datetime.date.today().year
    month = (request.args(1) is not None) and \
            request.args(1, cast=int) or datetime.date.today().month
    today = datetime.date.today()

    query = teacher_classes_query(auth.user_id)
    query &= ((db.student_classes.class_id==db.classes.id) &
              (db.student.id==db.student_classes.student_id) &
              (db.student.user_id==db.auth_user.id))

    data = db(query).select(db.student.id,
                            db.attendance.attendance_date,
                            db.attendance.present,
                            left=db.attendance.on(
                                (db.attendance.class_id==db.classes.id) &
                                (db.attendance.student_id==db.student.id) &
                                (db.attendance.attendance_date<=today)))

    return dict(data=data)
