# -*- coding: utf-8 -*-
# try something like
def index(): 
    grid = SQLFORM.smartgrid(db.student)
    return dict(grid=grid)
