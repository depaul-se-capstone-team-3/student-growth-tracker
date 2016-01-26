# -*- coding: utf-8 -*-
# requires authorized login to return classes
@auth.requires_login()
def index():
    """pull up teacher and classes that match current user and return a grid with the result"""
    if auth.has_membership(2, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))

    # declare constraints as where thea teacher matches an authorized user id
    constraints = db.gradebook.teacher == auth.user.id
    grid = db(constraints).select(join=db.gradebook.on(
        (db.gradebook.teacher==db.auth_user.id) & (db.gradebook.classes==db.classes.id)))
    # response.flash = 'Class List - %(first_name)s' % auth.user

    #class_data contains many classes, each class = [name, id, content_area, average]
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

# This should go under manage - assuming this is a school/district maanged tool,
# teachers won't add classes to their gradebooks.
def create():
    """generate form for new gradebook entry, redirect to index"""
    form = SQLFORM(db.gradebook).process(next=URL('index'))
    return dict(form=form)


def overview():
    if auth.has_membership(2, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))
    teacher_id = auth.user_id
    query = teacher_classes_query(teacher_id)
    class_names = db(query).select(db.classes.name)
    class_ids = db(query).select(db.classes.id)
    class_averages = []
    for cid in class_ids:
        total_score = get_class_total_score(cid)
        total_possible= get_class_total_possible(cid)
        average = 0
        try:
            average = round(total_score / total_possible * 100.0, 2)
            class_averages.append(average)
        except:
            pass
    
    
    
    return dict(class_names=class_names,
                class_averages=class_averages
               )
