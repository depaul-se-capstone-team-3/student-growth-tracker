# -*- coding: utf-8 -*-
# try something like
def index(): return dict(message="hello from notifications.py")

@auth.requires_login()
def detect_trends():
    if auth.has_membership(1, auth.user_id):
        pass
    else:
        redirect(URL('default','index'))
    detect_trends_scheduler()
    return dict(redirect(URL('admin','index')))
