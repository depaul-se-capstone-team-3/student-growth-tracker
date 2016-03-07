attendance_menu_items = []

if auth.has_membership('Teacher'):

    class_list = db((db.gradebook.teacher==auth.user_id) &
                    (db.gradebook.classes==db.classes.id)).select(db.classes.id,
                                                                  db.classes.name,
                                                                  orderby=db.classes.name)

    for class_ in class_list:
        attendance_menu_items.append((class_.name, False,
                                      URL('attendance', 'index', args=[class_.id]), []))

    response.menu += [(T('Attendance'), False, '', attendance_menu_items)]

if __name__ == '__main__':
    pass
