"""
Custom validators for the Student Growth Tracker application.
"""

from datetime import date


class STUDENTS_PRESENT(object):
    """
    Validator that determines whether students are in school on the given date.
    """
    def __init__(self, error_message='This is not a school day.'):
        self.error_message = error_message

    def __call__(self, value):
        value, err = IS_DATE()(value)
        if err:
            return (value, err)

        val, err = IS_NOT_IN_DB(db, 'students_not_present.date')(value)
        if err:
            return (value, self.error_message)
        elif value.weekday() >= 5:
            return (value, self.error_message)
        else:
            return (value, None)
