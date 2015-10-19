# -*- coding: utf-8 -*-
# try something like

def index():
    classes = SQLFORM.smartgrid(db.classes)
    return dict(classes=classes)


def create():
    form = SQLFORM(db.classes, submit_button='Create', labels = {'gradeLevel': 'Grade Level', 'startDate': 'Start Date', 'endDate': 'End Date'} ).process(next=URL('index'))
    return dict(form=form)
