#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @ Libresoft, December 2015

import os
from collections import namedtuple
import csv


class table_creator:

    def __init__(self):
        self.dicc_months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                        'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                        'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dic': '12', }
        self.dicc_version = {}
        # {'version': [version_id, family, date, size]}
        self.counter_version = 0
        self.dicc_module = {}
        # {'name': module_id, version_id}
        self.counter_module = 0
        self.dicc_submodule = {} # FIXME
        # {'name': submodule_id, module_id}
        self.counter_submodule = 0
        self.dicc_lang = {}
        # {'name': lang_id}
        self.counter_lang = 0
        self.dicc_file = {}
        # {'id': [name, path, sloc, lang_id, module_id, submodule_id, version_id]}
        self.counter_file = 0

        self.outf = "_outfile.dat"


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

    def get_module_id(self, module):

        module_id = 0
        if module in self.dicc_module.keys():
            module_id = self.dicc_module[module][0]
        else:
            self.counter_module += 1
            module_id = self.counter_module
            my_version = module.split("/")[2]
            version_id = self.dicc_version[my_version][0]
            self.dicc_module[module] = [module_id, version_id]
        return int(module_id)


    def get_submodule_id(self, submodule):

          submodule_id = 0
          if submodule in self.dicc_submodule.keys():
              submodule_id = self.dicc_submodule[submodule][0]
          else:
              module_in_sub = submodule.split("/")[:-1]
              module_in_sub = "/".join(module_in_sub)
              module_in_id = self.get_module_id(module_in_sub)
              self.counter_submodule += 1
              submodule_id = self.counter_submodule
              self.dicc_submodule[submodule] = [submodule_id, module_in_id]
          return int(submodule_id)

    def classify_path(self, path):

        list_paths = path.split("/")
        module_id = 0
        submodule_id = 0
        if len(list_paths) == 5:
            my_module = "/".join(list_paths)
            my_submodule = my_module # FIXME top_dir in both?
            module_id = self.get_module_id(my_module) # + '/top_dir'
            submodule_id = self.get_submodule_id(my_submodule)
        elif len(list_paths) == 6:
            my_module = "/".join(list_paths)
            submod_path = my_module #+ '/top_dir'
            module_id = self.get_module_id(my_module)
            submodule_id = self.get_submodule_id(submod_path)
        elif len(list_paths) > 6:
            my_module = "/".join(list_paths[:4])
            my_submodule = "/".join(list_paths[:5])
            module_id = self.get_module_id(my_module)
            submodule_id = self.get_submodule_id(my_submodule)
        else:
            my_module = "/".join(list_paths)
            my_submodule = my_module
            module_id = self.get_module_id(my_module)
            submodule_id = self.get_submodule_id(my_submodule)

        list_ids = [module_id, submodule_id]
        return list_ids


if __name__ == "__main__":

    print("\r\nTableCreator - Getting all data from slocdata (SLOCCount)\r\n")

    tcreator = table_creator()
    tcreator.fill_dicc_version('lkr-out.csv')

    os.chdir("slocdata")

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

                        tcreator.dicc_file[file_id] = [filename, path_short, sloc, lang_id, mod_id, submod_id, version_id]

    os.chdir("..")

    csv_file = open('file.csv', 'w')
    csv_version = open('version.csv', 'w')
    csv_module = open('module.csv', 'w')
    csv_submodule = open('submodule.csv', 'w')
    csv_lang = open('lang.csv', 'w')

    for x in tcreator.dicc_file.keys():
        aux = tcreator.dicc_file[x]
        list_new = []
        for item in aux:
            list_new.append(str(item))
        line = str(x) + "&" + "&".join(list_new)
        csv_file.write(line + "\r\n")

    for x in tcreator.dicc_version.keys():
        aux = tcreator.dicc_version[x]
        list_new = []
        for item in aux:
            list_new.append(str(item))
        line = str(x) + "&" + "&".join(list_new)
        csv_version.write(line + "\r\n")

    for x in tcreator.dicc_module.keys():
        aux = tcreator.dicc_module[x]
        list_new = []
        for item in aux:
            list_new.append(str(item))
        line = str(x) + "&" + "&".join(list_new)
        csv_module.write(line + "\r\n")

    for x in tcreator.dicc_submodule.keys():
        aux = tcreator.dicc_submodule[x]
        list_new = []
        for item in aux:
            list_new.append(str(item))
        line = str(x) + "&" + "&".join(list_new)
        csv_submodule.write(line + "\r\n")

    for x in tcreator.dicc_lang.keys():
        line = x + "&" + str(tcreator.dicc_lang[x])
        csv_lang.write(line + "\r\n")

    print("Output: csv's...Done\r\n\r\n")
