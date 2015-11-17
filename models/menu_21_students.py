if auth.has_membership('Student'):
    student_menu_items = [] # [(T('Classes'), False, URL('classes', 'index'), [])]

    class_list = db((db.student.user_id==auth.user_id) &
                    (db.student_classes.student_id==db.student.id) &
                    (db.student_classes.class_id==db.classes.id)).select(db.classes.id,
                                                                         db.classes.name)

    for class_ in class_list:
        student_menu_items.append((class_.name, False,
                                   URL('', 'overview', args=[class_.id]), []))

    response.menu += [(T('Classes'), False, '', student_menu_items)]

if __name__ == '__main__':
    pass
