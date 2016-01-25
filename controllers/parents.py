# -*- coding: utf-8 -*-
# try something like
@auth.requires_login()
def index(): 
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
 
             #
             #
             
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
    #need to get a parent_id. We also need a function to collect all students associated with a given parent_id.
    parent_id = auth.user_id
    #query holds list of students associated with the parent_id
    query = parent_student_query(parent_id)
    student_name = []
    students_info=[]
    student_ids =[]
    class_grades=[]
    standard_info=0
    #standard_dict={}
    student_standard_dict={}
    student_name_dict={}
    student_class_dict={}
    student_grade_dict={}
    unfinished_student_ids = db(query).select(db.student.id)
    snames = db(query).select(db.student.user_id)

    for r in unfinished_student_ids:
        student_ids.append(r.id)
    student_standard=[]
    student_classes=[]
    student_standards=[]

    #for every student associated with parent, parent_id.
    for r in student_ids:
        classes = get_student_classes(r)

        #for every class associated with the current student, r.
        for c in classes:
            student_classes.append(c.name)
            student_class_dict[r]=[c.id,c.name]
            grade = get_student_assignment_average(r,c.id)
            student_grade_dict[r]=[c.name,(grade[0]/grade[1]*100)]
            class_grades.append((grade[0]/grade[1])*100)
            #student_standard = get_standards_for_class(c.id)
            
            
            query = student_standards_query(r,c.id)
            standard_info = db(query).select(db.standard.id, db.standard.short_name, db.standard.reference_number,db.student_grade.student_score, db.grade.score)
            
            standard_dict={}
            for row in standard_info:
                if row.standard.id in standard_dict.keys():
                    if((row.grade.score != 0.0) | (row.student_grade.student_score != 0.0)):
                        max_score = standard_dict[row.standard.id][0] + row.grade.score
                        student_score = standard_dict[row.standard.id][1] + row.student_grade.student_score
                        standard_dict[row.standard.id] = [max_score, student_score, row.standard.reference_number, row.standard.short_name]
                else:
                    standard_dict[row.standard.id] = [row.grade.score, row.student_grade.student_score, row.standard.reference_number, row.standard.short_name]
            student_standard_dict[r]=standard_dict
            
            
            #add the standard.reference_numbers associated with the current class, c.
            for s in student_standard:
                student_standards.append(s.reference_number)

    #get the student names associated with parent, parent_id.
    i=0
    for s in snames:
        s_name={}
        name = get_student_name(s.user_id)
        s_name[i]=[name.first_name,name.last_name]
        student_name_dict[i]=[name.first_name,name.last_name]
        i+=1
        
        #s_name = get_student_name(s.user_id)
        #student_name.append(s_name.first_name)
        #student_name.append(s_name.last_name)


    return dict(student_name_dict=student_name_dict, student_class_dict=student_class_dict, class_grades=class_grades, student_standard=student_standard, student_standards=student_standards,standard_info=standard_info, student_standard_dict=student_standard_dict, student_grade_dict=student_grade_dict
               )
