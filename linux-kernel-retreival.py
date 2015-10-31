#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @ Libresoft, October 2015
import urllib.request
import os
import shutil
import sys
from urllib.parse import urlparse
from html.parser import HTMLParser

# Hay que coger tamaño del archivo, fecha, tamaño en bytes y numero de SLOC

INIT_PATH = os.path.abspath(os.curdir)
FOLDER_NAME = "linux_versions"
PRINT_TRACES = True
VERSIONS = ["v1.0", "v1.1", "v1.2", "v1.3", "v2.0", "v2.1", "v2.2", "v2.3", "v2.4", "v2.5", "v2.6", "v3.x", "v4.x"]
SEEN_URLS = []

class MyHTMLParser(HTMLParser):

    def handle_data(self, data):
        list_html.append(data)


def go_home_dir():
    """
    Goes back in current path to home directory
    """
    init_list = INIT_PATH.split('/')
    cur_dir = os.path.abspath(os.curdir)
    list_dir = cur_dir.split('/')
    exceeds = len(list_dir) - len(init_list)
    if exceeds > 0:
        if PRINT_TRACES:
            print("Going up ", str(exceeds)," directory levels")
        for i in range(exceeds):
            os.chdir('..')

def make_directories(versions):

    my_path = INIT_PATH + "/" + FOLDER_NAME
    os.mkdir(my_path.split("/")[-1])
    os.chdir(my_path)
    for version in versions:
        os.mkdir(version)

def remove_dir(directory):
    if os.path.exists(directory):
        if PRINT_TRACES:
            print ("Removing directory: ", directory)
        shutil.rmtree(directory, ignore_errors=True)


def getDownloadLinks(list_html_f, parser):

    urls_to_download = []
    for line in list_html_f: #list_html:
        if line[0] == "v":
            if line[:-1] != "v3.0":
                versions.append(line[:-1])

    if versions != VERSIONS:
        print("Wrong versions")
        raise SystemExit
    make_directories(versions)

    for version in versions:
        name = "linux-" + version[1:] + file_format
        download_url = kernel_url + version
        if PRINT_TRACES:
            print("Connecting to: ", download_url)
        response2 = urllib.request.urlopen(download_url)
        data2 = response2.read()
        html2_data = parser.feed(str(data2))

        for line2 in list_html:
            if line2.split("-")[0] == "linux":
                param = line2.split(".")
                if (param[-2] == "tar") and (param[-1] == "gz"):
                    my_index = list_html.index(line2)
                    new_index = my_index + 1
                    relevant_data = list_html[new_index].split()
                    date = relevant_data[0]
                    size_bytes = relevant_data[2]
                    final_url = download_url + "/" + line2
                    final_file = final_url.split("/")[-1]
                    if final_file not in SEEN_URLS:
                        SEEN_URLS.append(final_file)
                        urls_to_download.append([version, final_url, date, size_bytes])
                        if PRINT_TRACES:
                            print("Appending: ", version, " , ", final_url)

    return urls_to_download

def download_link(link, version):

    name = link.split("/")[-1]
    go_home_dir()
    os.chdir(FOLDER_NAME + "/" + version)
    if name in os.listdir(os.curdir):
        print("File already downloaded")
    else:
        if PRINT_TRACES:
            print("Downloading Version ", version, " - ", name)
        try:
            urllib.request.urlretrieve(link, name)
        except ContentTooShortError:
            print("Wrong URL: ", link)

        if not os.path.exists(name):
            print("Download failed", name)
    go_home_dir()

def handle_files():
    info_files = []
    for element in urls_to_download:
        act_version = element[0]
        url = element[1]
        file_name = download_link(url, act_version)
        get_info(file_name, info_files, act_version)
    return info_files

def make_report(data_list):
    go_home_dir()
    sizes = []
    file_output = open("lkr-out.csv", 'w')
    first_line = "Version,Name,Date,Size\r\n"
    file_output.write(first_line)
    urls_ready = []
    for field in data_list:
        version = field[0]
        name = field[1]
        urls_ready.append(name)
        date = field[2]
        size = field[3]
        sizes.append(size[:-1])
        line = version + ',' + name + ',' + date + ',' + size + "\r\n"
        file_output.write(line)
    file_output.close()
    print("Making report... Done")
    return urls_ready

if __name__ == "__main__":

    dw_again = False
    sh_param = sys.argv
    urls_ready = []
    if os.path.exists(FOLDER_NAME):
        if len(sh_param) > 1:
            if sh_param[1] == '-rm':
                remove_dir(FOLDER_NAME)
                dw_again = True
        else:
            try:
                lkr = open('lkr-out.csv', 'r')
                urls = lkr.readlines()
                urls = urls[1:]
                for url in urls:
                    urls_ready.append(url.split(",")[1])
                lkr.close()
            except IOError:
                raise SystemExit



    list_html = []
    file_format = ".tar.gz"
    kernel_url = "https://www.kernel.org/pub/linux/kernel/"
    versions = []

    if dw_again:
        response = urllib.request.urlopen(kernel_url)
        data = response.read()
        parser = MyHTMLParser()
        html_data = parser.feed(str(data))  # Fills list_html w/response
        urls_to_download = getDownloadLinks(list_html, parser)
        urls_ready = make_report(urls_to_download)

    go_home_dir()
    for url in urls_ready:
        version = url.split("/")[-2]
        download_link(url, version)
