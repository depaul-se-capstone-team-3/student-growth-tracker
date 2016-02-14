if auth.has_membership(1, auth.user_id):
    tools_menu_items = [("Add Teacher", False, URL("admin","teacher_create")),
                        ("Add Student", False, URL("admin","student_create")),
                        ("Add Class", False, URL("admin","classes_create")),
                        ("Add Parent", False, URL("admin","parent_create")),
                        ("Assign Teacher to Class", False, URL("admin","assign_teacher_to_class")),
                        ("Assign Student to Class", False, URL("admin","assign_student_to_class")),
                        ("Assign Parent to Student", False, URL("admin","assign_parent_to_student")),
                       ]
    views_menu_items = [("Standards Overview", False, URL("admin","standard_overview")),
                        ("Class List", False, URL("admin","class_list")),
                        ("Teacher List", False, URL("admin","teacher_list")),
                        ("Student List", False, URL("admin","student_list")),
                        ("Parent List", False, URL("admin","parent_list")),
                        ("Teacher - Class Relation", False, URL("admin","teacher_class")),
                        ("Student - Class Relation", False, URL("admin","student_class")),
                        ("Parent - Student Relation", False, URL("admin","parent_student")),
                        ]

    response.menu += [
        (T('Admin Tools'), False, "", tools_menu_items),
        (T('Admin Views'), False, "", views_menu_items),
    ]

if __name__ == '__main__':
    pass
