# -*- coding: utf-8 -*-
def index():
    grid = SQLFORM.smartgrid(db.grade)
    return locals()
