response.menu += [
    (T('Manage'), False, URL('manage', 'index'), [
        (T('Classes'), False, URL('manage', 'classes'), []),
        (T('Content Areas'), False, URL('manage', 'content_areas'), []),
        (T('Standards'), False, URL('manage', 'standards'), [])
    ])
]
