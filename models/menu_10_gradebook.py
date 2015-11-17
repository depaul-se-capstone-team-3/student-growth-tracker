if auth.has_membership(2, auth.user_id):
    response.menu += [
        (T('Grade Book'), False, URL('gradebook', 'index'), []),
    ]

if __name__ == '__main__':
    pass
