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
TABLE = 'version'
DICC_MONTHS = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dic': '12', }

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

def format_date(date):
    date_elem = date.split("-")
    day = date_elem[0]
    month = date_elem[1]
    year = date_elem[2]
    month_format = DICC_MONTHS[month]
    prop_date = [year, month_format, day]
    return "-".join(prop_date)

def form_insert_query(info_list, index, ntuple):

    my_row = ntuple(*info_list)
    date_ok = format_date(my_row.date)

    query = "INSERT INTO " + TABLE + " VALUES ("
    query += str(index) + ",'" + my_row.version + "',"
    query += str(my_row.size) + ",'" + my_row.group
    query += "','" + date_ok + "');"
    return query

def fill_version_table():
    lversion = namedtuple('Version', ['group', 'version', 'date', 'size'])
    lkrReader = csv.reader(open('lkr-out.csv'), delimiter=',', quotechar='|')
    cont = 0
    for row in lkrReader:
        cont += 1
        my_query = form_insert_query(row, cont, lversion)
        print "Running query: " + my_query
        run_query(my_query)

if __name__ == "__main__":

    print "Reading <lkr-out.csv> & register data into a DB\r\n"
    fill_version_table()
    print "...Done\r\n\r\n"
