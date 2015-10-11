# -*- coding: utf-8 -*-
# try something like
def index():
    grid = SQLFORM.smartgrid(db.contentarea)
    return locals()
