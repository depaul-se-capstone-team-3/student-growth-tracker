if auth.has_membership(1, auth.user_id):

    standards_menu_items = [('Building Standards Progress', False, URL('admin', 'standard_overview')),
                            ('Import Standards', False, URL('admin', 'standard_import'))]

    tools_menu_items = [('Activate Trend Dectection', False, URL('notifications','detect_trends')),
                        ('Trend Detection Settings', False, URL('admin','settings')),
                        ('Manage Teachers', False, URL('admin','teacher_create')),
                        ('Manage Students', False, URL('admin','student_create')),
                        ('Manage Classes', False, URL('admin','classes_create')),
                        ('Manage Parents', False, URL('admin','parent_create')),
                        ('Assign Teacher to Class', False, URL('admin','assign_teacher_to_class')),
                        ('Assign Student to Class', False, URL('admin','assign_student_to_class')),
                        ('Associate Parents with Students', False, URL('admin','assign_parent_to_student'))]

    views_menu_items = [('Teacher', False, URL('admin','teacher_list')),
                        ('Student', False, URL('admin','student_list')),
                        ('Classes', False, URL('admin','class_list')),
                        ('Parents', False, URL('admin','parent_list')),
                        ('Current Teachers\' Classes', False, URL('admin','teacher_class')),
                        ('Current Students\' Classes', False, URL('admin','student_class')),
                        ('Current Parents\' Students', False, URL('admin','parent_student'))]

    response.menu += [
        (T('Standards'), False, '', standards_menu_items),
        (T('Tools'), False, '', tools_menu_items),
        (T('Views'), False, '', views_menu_items),
    ]

if __name__ == '__main__':
    pass
