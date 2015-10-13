# -*- coding: utf-8 -*-
# try something like

def index(): 
    grid = SQLFORM.smartgrid(db.gradebook)
    # return dict(grid=grid)
    return locals()
