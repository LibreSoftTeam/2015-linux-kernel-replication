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
DB_NAME = 'linux_kernel_test'
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

def form_insert_version(info_list, ntuple):

    my_row = ntuple(*info_list)

    table = "version"
    query = "INSERT INTO " + table + " VALUES ("
    query += str(my_row.id) + ",'" + my_row.name + "','"
    query += my_row.family + "','" + my_row.date
    query += "'," + str(my_row.size) + ");"
    return query

def form_insert_module(info_list, ntuple):

    my_row = ntuple(*info_list)

    table = "module"
    query = "INSERT INTO " + table + " VALUES ("
    query += str(my_row.id) + ",'" + my_row.name + "',"
    query += str(my_row.version_id) + ");"
    return query

def form_insert_submodule(info_list, ntuple):

    my_row = ntuple(*info_list)

    table = "submodule"
    query = "INSERT INTO " + table + " VALUES ("
    query += str(my_row.id) + ",'" + my_row.name + "',"
    query += str(my_row.module_id) + ");"
    return query

def form_insert_lang(info_list, ntuple):

    my_row = ntuple(*info_list)

    table = "lang"
    query = "INSERT INTO " + table + " VALUES ("
    query += str(my_row.id) + ",'" + my_row.name + "');"
    return query

def form_insert_file(info_list, ntuple):

    my_row = ntuple(*info_list)

    table = "file"
    query = "INSERT INTO " + table + " VALUES ("
    query += str(my_row.id) + ",'" + my_row.name + "','" + my_row.path + "',"
    query += str(my_row.sloc) + "," + str(my_row.lang_id) + ","
    query += str(my_row.module_id) + "," + str(my_row.submodule_id) + ","
    query += str(my_row.version_id) + ");"
    return query

def fill_tables():

    lversion = namedtuple('Version', ['name', 'id', 'family', 'date', 'size'])
    versionReader = csv.reader(open('version.csv'), delimiter='&', quotechar='|')
    for row in versionReader:
        my_query = form_insert_version(row, lversion)
        print "Running query: " + my_query
        run_query(my_query)


    lmodule = namedtuple('Module', ['name', 'id', 'version_id'])
    modReader = csv.reader(open('module.csv'), delimiter='&', quotechar='|')
    for row in modReader:
        my_query = form_insert_module(row, lmodule)
        print "Running query: " + my_query
        run_query(my_query)


    lsubmodule = namedtuple('Submodule', ['name', 'id', 'module_id'])
    submodReader = csv.reader(open('submodule.csv'), delimiter='&', quotechar='|')
    for row in submodReader:
        my_query = form_insert_submodule(row, lsubmodule)
        print "Running query: " + my_query
        run_query(my_query)

    llang = namedtuple('Lang', ['name', 'id'])
    langReader = csv.reader(open('lang.csv'), delimiter='&', quotechar='|')
    for row in langReader:
        my_query = form_insert_lang(row, llang)
        print "Running query: " + my_query
        run_query(my_query)

    lfile = namedtuple('File', ['id', 'name', 'path', 'sloc', 'lang_id', 'module_id', 'submodule_id', 'version_id'])
    fileReader = csv.reader(open('file.csv'), delimiter='&', quotechar='|')
    for row in fileReader:
        my_query = form_insert_file(row, lfile)
        print "Running query: " + my_query
        run_query(my_query)

if __name__ == "__main__":

    print "Reading csv's & register data into a DB\r\n"
    fill_tables()
    print "...Done\r\n\r\n"
