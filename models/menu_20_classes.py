classes_menu_items = [] # [(T('Classes'), False, URL('classes', 'index'), [])]

if auth.has_membership(2, auth.user_id):
    class_list = db((db.gradebook.teacher==auth.user_id) &
                    (db.gradebook.classes==db.classes.id)).select(db.classes.id,
                                                                  db.classes.name)

    for class_ in class_list:
        classes_menu_items.append((class_.name, False,
                                   URL('classes', 'overview', args=[class_.id]), []))

#elif auth.has_membership(3, auth.user_id):
#    class_list = db((db.student.user_id==auth.user_id) &
#                    (db.student_classes.class_id==db.classes.id) &
#                    (db.student_classes.student_id==db.student.user_id)).select(db.classes.id,
#                                                                  db.classes.name, db.student.id)

#    for class_ in class_list:
#        classes_menu_items.append((class_.name, False,
#                                   URL('students', 'index', args=[class_.id]), []))

response.menu += [(T('Classes'), False, '', classes_menu_items)]

if __name__ == '__main__':
    pass
