"""
The attendance controller.

"""
import datetime

@auth.requires(auth.has_membership(role='Teacher'), requires_login=True)
def index():
    """
    Attendance information for a class.
    """
    pass
