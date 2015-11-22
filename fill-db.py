#!/usr/bin/python
# -*- coding: utf-8 -*-

# @ Libresoft, November 2015
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

    conn = MySQLdb.connect(*datos) # Connect to Database
    cursor = conn.cursor()         # Create cursor
    cursor.execute(query)          # Run a query

    if query.upper().startswith('SELECT'):
        data = cursor.fetchall()   # Bring SELECT results
    else:
        conn.commit()              # Make data writing effective
        data = None

    cursor.close()                 # Close cursor
    conn.close()                   # Close connection

    return data


if __name__ == "__main__":

    print "Reading <lkr-out.csv> & register data into a DB\r\n"
    Version = namedtuple('Version', ['group', 'version', 'size', 'sloc'])
    lkrReader = csv.reader(open('lkr-out.csv'), delimiter=',', quotechar='|')
    for row in lkrReader:
        group = row[0]
        version = row[1]
        size = row[2]
        sloc = row[3]
        query = "INSERT INTO " + TABLE + " VALUES ('" + group + "','" + version
        query += "'," + str(size) + "," + str(sloc) + ");"
        run_query(query)
    print "...Done\r\n\r\n"
