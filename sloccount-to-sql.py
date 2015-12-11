#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @ Libresoft, December 2015

import os
from collections import namedtuple
import csv
import pymysql.cursors

# TODO: Check and improve functions

def form_insert_version(info_list, ntuple):

    my_row = ntuple(*info_list)

    table = "versions"
    query = "INSERT INTO " + table + " VALUES ("
    query += str(my_row.id) + ",'" + my_row.name + "','"
    query += my_row.family + "','" + my_row.date
    query += "'," + str(my_row.size) + ");"
    return query

def form_insert_module(info_list, ntuple):

    my_row = ntuple(*info_list)

    table = "modules"
    query = "INSERT INTO " + table + " VALUES ("
    query += str(my_row.id) + ",'" + my_row.name + "');"
    return query

def form_insert_submodule(info_list, ntuple):

    my_row = ntuple(*info_list)

    table = "submodules"
    query = "INSERT INTO " + table + " VALUES ("
    query += str(my_row.id) + ",'" + my_row.name + "');"
    return query

def form_insert_lang(info_list, ntuple):

    my_row = ntuple(*info_list)

    table = "langs"
    query = "INSERT INTO " + table + " VALUES ("
    query += str(my_row.id) + ",'" + my_row.name + "');"
    return query

def form_insert_file(info_list, ntuple):

    my_row = ntuple(*info_list)

    table = "files"
    query = "INSERT INTO " + table + " VALUES ("
    query += str(my_row.id) + ",'" + my_row.name + "','" + my_row.path + "',"
    query += str(my_row.sloc) + "," + str(my_row.lang_id) + ","
    query += str(my_row.module_id) + "," + str(my_row.submodule_id) + ","
    query += str(my_row.version_id) + ");"
    return query


class table_creator:

    def __init__(self):
        self.dicc_months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                        'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                        'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12', }
        self.dicc_version = {}
        # {'version': [version_id, family, date, size]}
        self.counter_version = 0
        self.dicc_module = {}
        # {'name': module_id}
        self.counter_module = 0
        self.dicc_submodule = {} # FIXME
        # {'name': submodule_id}
        self.counter_submodule = 0
        self.dicc_lang = {}
        # {'name': lang_id}
        self.counter_lang = 0
        self.dicc_file = {}
        # {'id': [name, path, sloc, lang_id, module_id, submodule_id, version_id]}
        self.counter_file = 0

        self.outf = "_outfile.dat"
        self.connection = pymysql.connect(host='localhost',
                                     user='operator',
                                     password='operator',
                                     db='lktest',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

    def intro_query(self, query):


        with self.connection.cursor() as cursor:
            # Create a new record
            cursor.execute(query)
        self.connection.commit()

    def read_response(self, answer):

        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT 'id', 'password' FROM 'users' WHERE 'email'=%s"
                cursor.execute(sql, ('webmaster@python.org',))
                result = cursor.fetchone()
                print(result)
        finally:
            self.connection.close()

    def format_date(self, date):
        date_elem = date.split("-")
        day = date_elem[0]
        month = date_elem[1]
        year = date_elem[2]
        month_format = self.dicc_months[month]
        prop_date = [year, month_format, day]
        return "-".join(prop_date)


    def fill_dicc_version(self, csvname):
        lversion = namedtuple('Version', ['family', 'version', 'date', 'size'])
        lkrReader = csv.reader(open(csvname), delimiter=',', quotechar='|')
        for row in lkrReader:
            my_row = lversion(*row)
            date_ok = self.format_date(my_row.date)
            self.counter_version += 1
            version_id = self.counter_version
            self.dicc_version[my_row.version] = [version_id, my_row.family, date_ok, my_row.size]

    def get_lang_id(self, lang):

        lang_id = 0
        if lang in self.dicc_lang.keys():
            lang_id = self.dicc_lang[lang]
        else:
            self.counter_lang += 1
            lang_id = self.counter_lang
            self.dicc_lang[lang] = lang_id
        return int(lang_id)

    def get_module_id(self, my_module):
        module_id = 0
        module = my_module.split('/')[-1]
        if module in self.dicc_module.keys():
            module_id = self.dicc_module[module]
        else:
            self.counter_module += 1
            module_id = self.counter_module
            self.dicc_module[module] = module_id

        return int(module_id)


    def get_submodule_id(self, my_submodule):

        submodule_id = 0
        submodule = my_submodule.split('/')[-1]
        if submodule in self.dicc_submodule.keys():
            submodule_id = self.dicc_submodule[submodule]
        else:
            self.counter_submodule += 1
            submodule_id = self.counter_submodule
            self.dicc_submodule[submodule] = submodule_id
        return int(submodule_id)

    def classify_path(self, path):

        list_paths = path.split("/")
        module_id = 0
        submodule_id = 0
        if len(list_paths) == 5:
            my_module = "/".join(list_paths)
            my_submodule = my_module + '/top_dir'
            module_id = self.get_module_id(my_module)
            submodule_id = self.get_submodule_id(my_submodule)

        elif len(list_paths) == 6:
            my_module = "/".join(list_paths[:-1])
            submod_path = my_module + "/" + list_paths[-1]
            module_id = self.get_module_id(my_module)
            submodule_id = self.get_submodule_id(submod_path)

        elif len(list_paths) > 6:

            my_module = "/".join(list_paths[:5])
            my_submodule = "/".join(list_paths[:6])
            module_id = self.get_module_id(my_module)
            submodule_id = self.get_submodule_id(my_submodule)

        else:
            my_module = "/".join(list_paths) + '/top_dir'
            my_submodule = my_module + '/top_dir'
            module_id = self.get_module_id(my_module)
            submodule_id = self.get_submodule_id(my_submodule)

        list_ids = [module_id, submodule_id]
        return list_ids


if __name__ == "__main__":

    print("\r\nTableCreator - Getting all data from slocdata (SLOCCount)\r\n")

    tcreator = table_creator()
    tcreator.fill_dicc_version('lkr-out.csv')
    sql_file = open('files.sql', 'w')

    os.chdir("slocdata")
    lfile = namedtuple('File', ['id', 'name', 'path', 'sloc', 'lang_id', 'module_id', 'submodule_id', 'version_id'])
    outf = "_outfile.dat"
    for (path, dirs, files) in os.walk(os.curdir):
        if files != []:
            imp_files = [item for item in files if outf in item]
            if imp_files != []:
                my_path = path
                for out_file in imp_files:
                    try:
                        my_file = open(my_path + "/" + out_file, 'r')
                    except FileNotFoundError:
                        raise SystemExit
                    lines = [line for line in my_file.readlines() if len(line.split(" "))>1]
                    my_file.close()
                    for line in lines:
                        line_list = line.split(" ")
                        sloc = int(line_list[0])
                        path = line_list[-1]
                        path_short = path.split("linux_versions")[1]
                        path_short = path_short.split("/")[:-1]
                        path_short = "/".join(path_short)

                        list_ids = tcreator.classify_path(path_short)

                        mod_id = list_ids[0]
                        submod_id = list_ids[1]
                        filename = path.split("/")[-1][:-1]
                        lang = out_file.split("_outfile.dat")[0]
                        lang_id = tcreator.get_lang_id(lang)
                        version_id = tcreator.dicc_version[my_path.split("/")[1]][0]
                        tcreator.counter_file += 1
                        file_id = tcreator.counter_file

                        file_info = [file_id, filename, path_short, sloc,
                                     lang_id, mod_id, submod_id, version_id]
                        my_query = form_insert_file(file_info, lfile)
                        sql_file.write(my_query + "\r\n")


    sql_file.close()
    os.chdir("..")

    lversion = namedtuple('Version', ['name', 'id', 'family', 'date', 'size'])

    for x in tcreator.dicc_version.keys():
        aux = tcreator.dicc_version[x]
        row = [str(x)]
        for item in aux:
            row.append(str(item))
        print(row)
        my_query = form_insert_version(row, lversion)
        print("Running query: " + my_query)
        tcreator.intro_query(my_query)

    lmodule = namedtuple('Module', ['name', 'id'])
    for x in tcreator.dicc_module.keys():
        aux = tcreator.dicc_module[x]
        row = [str(x), str(aux)]
        print(row)
        my_query = form_insert_module(row, lmodule)
        print("Running query: " + my_query)
        tcreator.intro_query(my_query)

    lsubmodule = namedtuple('Submodule', ['name', 'id'])
    for x in tcreator.dicc_submodule.keys():
        aux = tcreator.dicc_submodule[x]
        row = [str(x), str(aux)]
        print(row)
        my_query = form_insert_submodule(row, lsubmodule)
        print("Running query: " + my_query)
        tcreator.intro_query(my_query)

    llang = namedtuple('Lang', ['name', 'id'])
    for x in tcreator.dicc_lang.keys():
        aux = tcreator.dicc_lang[x]
        row = [str(x), str(aux)]
        print(row)
        my_query = form_insert_lang(row, llang)
        print("Running query: " + my_query)
        tcreator.intro_query(my_query)

    print("Output: Entering files data in database...\r\n\r\n")

    tcreator.connection.close()
    os.system("mysql -u operator -poperator lktest < files.sql")
    print("...Done\r\n\r\n")
