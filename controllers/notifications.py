# -*- coding: utf-8 -*-
# try something like
def index(): return dict(message="hello from notifications.py")

@auth.requires_login()
def detect_trends():
    detect_trends_scheduler()
    return dict(redirect(URL('admin','index')))
