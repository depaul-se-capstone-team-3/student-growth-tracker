# -*- coding: utf-8 -*-
import copy
import os.path

test_db = DAL('sqlite://testing.sqlite')
for tablename in db.tables:  # Copy tables!
    table_copy = [copy.copy(f) for f in db[tablename]]
    test_db.define_table(tablename, *table_copy)

