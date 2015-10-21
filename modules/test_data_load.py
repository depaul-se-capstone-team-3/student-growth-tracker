#!/usr/bin/env python2
"""
=================
test_data_load.py
=================

.. rubric:: A script for importing dummy data.
"""
import argparse
import csv
import glob
import os.path
import re

# from gluon import DAL, Field

def get_table_name_from_file_name(file_name):
    """
    Extract the table name from the data file name.

    The file name must conform to a specific format. At some point we might make
    this more flexible, but for now we're going to do this.

    Format: ``load_xx_table_name_dummy.csv``
    where ``xx`` is a two-digit code that defines the load order for the data.
    """
    table_name = re.search(r'load_\d\d_db_(\w+)_dummy.csv', file_name).group(1)
    table = 'db.%s' % table_name
    return table
    

def get_data_file_list(data_dir):
    """
    Read the list of data files from the ``data_dir``.

    The file names determine the sort order.
    See :function:`get_table_name_from_file_name` for information on the correct
    format for data file names.
    """
    data_dir = data_dir and data_dir.endswith('/') or data_dir + '/'
    file_list = glob.glob(data_dir + '*')
    return file_list

def _parse_arguments():
    parser = argparse.ArgumentParser(description='Data Import')
    parser.add_argument('-s', '--source-directory', default='./data',
                        help='Where the files are.')
    parser.add_argument('-d', '--delimiter', default=',',
                        help='The field delimiter.')
    arg
    
    return parser.parse_args()

def main():
    args = _parse_arguments()
    data_dir = '%s' % args.source_directory
    file_list = None
    if os.path.exists(data_dir):
        file_list = get_data_file_list(data_dir)

    for data_file in file_list:
        table_name = get_table_name_from_file_name(data_file)
        print 'Parsing %s' % table_name

        with open(data_file, 'r') as infile:
            data_reader = csv.reader(infile)
            headers = data_reader.next()
            print ' | '.join(headers)
            for row in data_reader:
                print ' | '.join(row)

            print ''

if __name__ == '__main__':
    main()



# for data_file in glob.glob(data):
#     table_name = re.search(r'load_\d\d_db_(\w+)_dummy.csv', data_file).group(1)
#     table = 'db.%s' % table_name
#     print 'Populating %s' % table

#     if db(table).isempty():
#         print '%s is empty.' %table
#     else:
#         print '%s is not empty - skipping load.' % table

# if db(db.auth_user).isempty():
#     teacher_id = db.auth_user.insert(first_name='Bob',last_name='Johnson',
#                                      username='bobjohnson',
#                                      email='bob.johnson@example.com',
#                                      password=CRYPT()('test')[0])
