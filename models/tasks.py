# -*- coding: utf-8 -*-

def detect_trends_scheduler():
    trend_num_query = db(db.settings.location == "trend").select(db.settings.setting)
    trend_num = trend_num_query[0].setting

    students_query = (db.student.id> 0)
    students = db(students_query).select(db.student.id)
    student_count = 0
    class_count = 0
    assignment_count = 0
    assignment_list = []
    student_average_values_list = []
    for student in students:
        student_count += 1
        class_query = ((db.student_classes.student_id == student.id)&
                       (db.student_classes.class_id == db.classes.id))
        classes = db(class_query).select(db.classes.id)
        count_i = 0
        count_j = 0
        count_k = 0
        assignment_dict = {}
        
        for single_class in classes:
            class_count += 1
            assignments = assignments = get_student_assignment_list(student.id, single_class.id)
            student_score= 0
            student_possible = 0
            student_missing_assignments = 0
            missing_assignment_list=[]
            individual_assignment_count=0
            for assignment in assignments:
                assignment_count +=1
                individual_assignment_count += 1
                student_score = assignment.student_grade.student_score
                student_possible += assignment.grade.score
                grade_info = [assignment.grade.name, assignment.student_grade.student_score, assignment.grade.score]
                assignment_list.append(grade_info)
                if (student_score == 0):
                    missing_assignment_list.append(assignment.grade.due_date)
                    student_missing_assignments += 1
            average_values = [student.id, single_class.id, student_score, student_possible]
            student_average_values_list.append(average_values)
            student_average = student_score/student_possible
            if (student_average < trend_num/100.0):
                db.notifications.insert(student_id=student.id,
                                        class_id=single_class.id,
                                        date=datetime.datetime.today().date(),
                                        warning_text=("Student Grade is less than "+ str(trend_num) + "%."))
            if (student_missing_assignments > 5):
                db.notifications.insert(student_id=student.id,
                                        class_id=single_class.id,
                                        date=datetime.datetime.today().date(),
                                        warning_text=("Student is missing excessive grades."))
            if(len(missing_assignment_list)>2):
                miss_list = sorted(missing_assignment_list)
                i = -1
                j = 0
                miss_total = 0
                for miss in miss_list:
                    if i == -1:
                        i+=1
                        j+=1
                        continue
                    times = miss_list[i] - miss_list[j]
                    if times.days >= -1 & times.days < 0:
                        miss_total +=1
                    elif miss_total < 2:
                        miss_total = 0
                    elif miss_total >= 2:
                        break
                    i+=1
                    j+=1

                if(miss_total > 0):
                    db.notifications.insert(student_id=student.id,
                                        class_id=single_class.id,
                                        date=datetime.datetime.today().date(),
                                        warning_text=("two or more consecutive missing assignments ("+str(miss_total+1)+")"))
            
    session.flash="Trend Database Populated with New Warnings."
    #returns are largely still for testing purposes
#    return dict(student_count=student_count,
#                 class_count=class_count,
#                 assignment_count=assignment_count,
#                 assignment_dict=assignment_dict,
#                 assignment_list=assignment_list,
#                 student_average_values_list=student_average_values_list
#                 )
    db.commit()
    return 1


from gluon.scheduler import Scheduler
Scheduler(db, dict(detect_trends_scheduler=detect_trends_scheduler))
