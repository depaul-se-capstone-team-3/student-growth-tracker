# -*- coding: utf-8 -*-
# try something like
@auth.requires_login()
def index(): 
    if auth.has_membership(4, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))
    parent_id = auth.user_id
    #setup query of students linked to the parent_id
    student_ids_query = ((db.auth_user.id == parent_id) &
                         (db.auth_user.id == db.parent_student.parent_id) &
                         (db.parent_student.student_id == db.student.id))
    student_ids = db(student_ids_query).select(db.student.id, db.student.user_id)
    student_id_dict = {}
    student_name_dict = {}
    full_dict = {}

    for student in student_ids:
        #student_id_dict[student.id] = student.user_id
        #set up query to pull back classes a student is in.
        student_classes_query = ((db.student.id==student.id)&
                                 (db.student.id == db.student_classes.student_id)&                                             (db.student_classes.class_id==db.classes.id))

        student_classes = db(student_classes_query).select(db.classes.id, db.classes.name)
         
        student_name = get_student_name(student.user_id)
        name = student_name.first_name + " " + student_name.last_name
        student_name_dict[student.id] = name
        student_class_and_average_dict = {}
        class_list = []
        i = 0
        class_dict = {}
         
        for student_class in student_classes:
            #student_id_dict[student.id] = student_class.name
            #get student class average
            student_average_list = get_student_assignment_average(student.id, student_class.id)
            student_average = student_average_list[0]/student_average_list[1] * 100
            #does this need to be a dict?
            #dict1 = {student_class.name: student_average}
            new_dict = {'blort':'blortyblort'}
            dict1 = {}
            dict1[student_class.name] = [student_average, new_dict]
            class_list.append(dict1)
            i += 1
            #student_id_dict = {student.id: class_list}
            student_id_dict[student.id] = class_list
             
            student_standards = student_standards_query(student.id, student_class.id)
             
            standard_info = db(student_standards).select(db.standard.id, db.standard.short_name, db.standard.reference_number,db.student_grade.student_score, db.grade.score)
             
            standard_dict={}
            for row in standard_info:
                if row.standard.id in standard_dict.keys():
                    if((row.grade.score != 0.0) | (row.student_grade.student_score != 0.0)):
                        max_score =  standard_dict[row.standard.id][0] + row.grade.score 
                        student_score = standard_dict[row.standard.id][1] + row.student_grade.student_score
                        standard_dict[row.standard.id] = [max_score, student_score,                                                                     row.standard.reference_number,row.standard.short_name]
                else:
                    standard_dict[row.standard.id] = [row.grade.score,
                                                     row.student_grade.student_score,
                                                     row.standard.reference_number,
                                                     row.standard.short_name]

            class_dict[student_class.name] = [student_average, standard_dict]
            full_dict[name] = class_dict
            """
            if student.id in student_class_and_average_dict:
                student_class_and_average_dict[student.id].append(student_class.name)
            else:
                student_class_and_average_dict[student.id] = student_class.name
            """
 
    return dict(student_id_dict=student_id_dict,
                student_classes=student_classes,
                class_list=class_list,
                standard_info=standard_info,
                student_standards=student_standards,
                student_name_dict=student_name_dict,
                standard_dict=standard_dict,
                full_dict=full_dict)

@auth.requires_login()
def overview():
    if auth.has_membership(4, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))
    parent_id = auth.user_id
    query = (db.auth_user.id == parent_id)
    parent_name = db(query).select(db.auth_user.first_name, db.auth_user.last_name)
    for row in parent_name:
        parent_name = row.first_name + " " + row.last_name
    #setup query of students linked to the parent_id
    student_ids_query = ((db.auth_user.id == parent_id) &
                         (db.auth_user.id == db.parent_student.parent_id) &
                         (db.parent_student.student_id == db.student.id))
    student_ids = db(student_ids_query).select(db.student.id, db.student.user_id)
    student_id_dict = {}
    student_name_dict = {}
    full_dict = {}
    
    for student in student_ids:
        #student_id_dict[student.id] = student.user_id
        #set up query to pull back classes a student is in.
        student_classes_query = ((db.student.id==student.id)&
                                 (db.student.id == db.student_classes.student_id)&                                                (db.student_classes.class_id==db.classes.id))
    
        student_classes = db(student_classes_query).select(db.classes.id, db.classes.name)
        
        student_name = get_student_name(student.user_id)
        name = student_name.first_name + " " + student_name.last_name
        student_name_dict[student.id] = name
        student_class_and_average_dict = {}
        class_list = []
        i = 0
        class_dict = {}
        
        for student_class in student_classes:
            #student_id_dict[student.id] = student_class.name
            #get student class average
            student_average_list = get_student_assignment_average(student.id, student_class.id)
            student_average = student_average_list[0]/student_average_list[1] * 100
            #does this need to be a dict?
            #dict1 = {student_class.name: student_average}
            new_dict = {'blort':'blortyblort'}
            dict1 = {}
            dict1[student_class.name] = [student_average, new_dict]
            class_list.append(dict1)
            i += 1
            #student_id_dict = {student.id: class_list}
            student_id_dict[student.id] = class_list
            
            student_standards = student_standards_query(student.id, student_class.id)
            
            standard_info = db(student_standards).select(db.standard.id, db.standard.short_name, db.standard.reference_number,db.student_grade.student_score, db.grade.score)
            #create empty standard dictionary
            standard_dict={}
            #for each row returned by the query...
            for row in standard_info:
                #if the standard is already in the dictionary...
                if row.standard.id in standard_dict.keys():
                    #make sure neither score is zero (error avoidance)
                    if((row.grade.score != 0.0) | (row.student_grade.student_score != 0.0)):
                        #set max score to the current standard cumulative score plus whatever the score is for the row
                        max_score = standard_dict[row.standard.id][0] + row.grade.score
                        #set new student score in the same basic way
                        student_score = standard_dict[row.standard.id][1] +                                                                         row.student_grade.student_score
                        #overwrite the standard to have [new max score, new student score, ref num and short name
                        standard_dict[row.standard.id] = [max_score, student_score,                                                                     row.standard.reference_number,                                                                 row.standard.short_name]
                else:
                    #otherwise, add the key to the dictionary with the information.
                    standard_dict[row.standard.id] = [row.grade.score,
                                                      row.student_grade.student_score,
                                                      row.standard.reference_number,
                                                      row.standard.short_name]

            
            class_dict[student_class.name] = [student_average, standard_dict]
            full_dict[name] = class_dict
            """
            if student.id in student_class_and_average_dict:
                student_class_and_average_dict[student.id].append(student_class.name)
            else:
                student_class_and_average_dict[student.id] = student_class.name
            """

    return dict(full_dict=full_dict,
                 standard_info=standard_info,
                 parent_name=parent_name)
