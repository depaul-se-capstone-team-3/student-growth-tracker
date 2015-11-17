if auth.has_membership('Teacher'):
    classes_menu_items = []

    class_list = db((db.gradebook.teacher==auth.user_id) &
                    (db.gradebook.classes==db.classes.id)).select(db.classes.id,
                                                                  db.classes.name)

    for class_ in class_list:
        classes_menu_items.append((class_.name, False,
                                   URL('classes', 'overview', args=[class_.id]), []))

    response.menu += [(T('Classes'), False, '', classes_menu_items)]

if __name__ == '__main__':
    pass
