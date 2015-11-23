#!/usr/bin/python
# -*- coding: utf-8 -*-

# @ Libresoft, November 2015
# TODO Make this script for Python3

import csv
from collections import namedtuple
import MySQLdb

DB_HOST = 'localhost'
DB_USER = 'operator'
DB_PASS = 'operator'
DB_NAME = 'lkr'
TABLE = 'lkr_out'


def run_query(query=''):
    datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME]

    conn = MySQLdb.connect(*datos)  # Connect to Database
    cursor = conn.cursor()          # Create cursor
    cursor.execute(query)           # Run a query

    if query.upper().startswith('SELECT'):
        data = cursor.fetchall()   # Bring SELECT results
    else:
        conn.commit()              # Make data writing effective
        data = None

    cursor.close()                 # Close cursor
    conn.close()                   # Close connection

    return data


def form_insert_query(info_list, ntuple):

    my_row = ntuple(*info_lists)
    query = "INSERT INTO " + TABLE + " VALUES ('"
    query += my_row.group + "','" + my_row.version
    query += "'," + str(my_row.size) + "," + str(my_row.sloc) + ");"
    return query


if __name__ == "__main__":

    print "Reading <lkr-out.csv> & register data into a DB\r\n"
    lversion = namedtuple('Version', ['group', 'version', 'size', 'sloc'])
    lkrReader = csv.reader(open('lkr-out.csv'), delimiter=',', quotechar='|')

    for row in lkrReader:
        my_query = form_insert_query(row, lversion)
        print "Running query: " + query
        run_query(query)

    print "...Done\r\n\r\n"
