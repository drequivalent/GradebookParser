import os
import os.path
import lxml.html
###############################################################
#IMPORTANT NOTE: bundling on windows
###############################################################
#The setup.py file for this thing looks something like this:
#
#from distutils.core import setup
#import py2exe, sys, os
#sys.argv.append('py2exe')
#setup(
#    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
#    windows = [{'script': "marx.py"}],
#    zipfile = None,
#)
#
#Before bundling, install stuptools, py2exe and lxml.
#Bundling command: python setup.py py2exe -p lxml,gzip
###############################################################
#PARSING ZONE: where the actual fun happens
###############################################################

def assemble_table(string):
    """Assembles the table (list-of-lists) that contains dates, topics and lesson contents from HTML string"""
    doc = lxml.html.document_fromstring(string)
    listlist = [["Date", "Topic", "Content"]]
    for element in doc.find_class("group-header lesson-theme st0"):
        stringlist = []
        stringlist.append(element.attrib["datelesson"].encode('utf8'))
        stringlist.append(element.attrib["theme"].strip().replace("\n", "//").encode('utf8'))
        stringlist.append(squeeze_string(element.attrib["contentlesson"].strip().replace("\n", "//").encode('utf8'), "//"))
        listlist.append(stringlist)
    return listlist

def assemble_csv(listlist):
    """Assemblse semicolon-separated CSV table from the list-of-lists, and returns a string"""
    strings = []
    for string in listlist:
        strings.append(";".join(string))
    filestring = "\n".join(strings)
    return filestring

###############################################################
#LITTLE TWEAKS ZONE: small utilities that are nice to have
###############################################################

def squeeze_string(string, char):
    """Squeezes off repeating characters without using regular expressions"""
    while char*2 in string:
        string=string.replace(char*2,char)
    return string

###############################################################
#DANGER ZONE: this thing writes to real files. Handle with care
###############################################################

def create_input_and_output_dirs(root = os.curdir, inputdirname = "Input", outputdirname = "Output"):
    fullroot = os.path.expanduser(root)
    inputdirpath = os.sep.join([fullroot, inputdirname])
    outputdirpath = os.sep.join([fullroot, outputdirname])
    if not os.path.exists(inputdirpath):
        os.makedirs(inputdirpath)
    if not os.path.exists(outputdirpath):
        os.makedirs(outputdirpath)

def list_input_directory(root = os.curdir, inputdirname = "Input"):
    fullroot = os.path.expanduser(root)
    inputdirpath = os.sep.join([fullroot, inputdirname])
    resultlist = []
    for item in os.listdir(inputdirpath):
        resultlist.append(os.sep.join([inputdirpath, item]))
    return resultlist

def process_the_input_file(filepath, root = os.curdir, outputdirname = "Output"):
    if os.path.isfile(filepath):
        string = open(filepath).read()
        string = assemble_csv(assemble_table(string))
        basename = os.path.split(filepath)[-1] + ".csv"
        outfile = open(os.sep.join([outputdirname, basename]), "w")
        outfile.write(string)
        outfile.close()
    else:
        return

def process_all_input(root = os.curdir, inputdirname = "Input", outputdirname = "Output"):
    for path in list_input_directory(root, inputdirname):
        process_the_input_file(path, root, outputdirname)

create_input_and_output_dirs()
process_all_input()

