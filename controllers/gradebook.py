# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    """
    Pull up teacher and classes that match
    current user and return a grid with the result.
    """
    if auth.has_membership(2, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))

    # declare constraints as where thea teacher matches an authorized user id
    constraints = db.gradebook.teacher == auth.user.id
    grid = db(constraints).select(
        join=db.gradebook.on(
            (db.gradebook.teacher==db.auth_user.id) &
            (db.gradebook.classes==db.classes.id)))

    # class_data contains many classes,
    # each class = [name, id, content_area, average]
    class_data = []
    for row in grid:
        average = 0
        try:
            average = format(get_class_total_score(row.classes.id) /
                             get_class_total_possible(row.classes.id) * 100.00, '.2f')
        except:
            pass

        single_class=[row.classes.name, row.classes.id, row.classes.content_area.name, average]
        class_data.append(single_class)

    return dict(class_data=class_data)
