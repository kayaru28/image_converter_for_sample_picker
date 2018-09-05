import csv
import os
import sys
import numpy as np
import pandas as pd

ERROR_CODE  = 100
NORMAL_CODE = 0

def left(str, amount):
    return str[:amount]

def right(str, amount):
    return str[-amount:]

def mid(str, offset, amount):
    return str[offset:offset+amount]

def max(a,b):
    ans = a
    if( a < b ):
        ans = b
    return ans

def min(a,b):
    ans = a
    if( a > b ):
        ans = b
    return ans

def cutStrBeforeKey(key,str):
    no  = patternMatch(key,str)
    ans = left( str , no - 1) 
    return ans

def cutStrAfterKey(key,str):
    no  = patternMatch(key,str)
    no  = no + ( len(key) - 1 )
    ans = right( str , len(str) - no )
    return ans

def patternMatch(key,str):
    # 一致する　：＞0
    # 一致しない：＝0
    ans = str.find(key) + 1
    return ans

def judgeError(exit_code):
    if exit_code == ERROR_CODE:
        print("!!!!ERROR OCCURED!!!!11!!")
        sys.exit()

def get_script_dir():
    return os.path.abspath(os.path.dirname(__file__))

###########################################################
#
# varidation
#
###########################################################

def isNotNull(str):
    ans = True

    if(str == None):
        ans = False
    elif(str == ""):
        ans = False
    return ans

def isNull(str):
    ans = False
    if(str == None):
        ans = True
    elif(str == ""):
        ans = True
    return ans

###########################################################
#
# read and write for csv
#
###########################################################

class CsvWriter():
    file = ""

    def openFile(self,file_path):
        if isNull(file_path):
            print(" input file_name ")
            return ERROR_CODE

        if not os.path.exists(file_path):
            print(" do not exist that file " + file_path)
            return ERROR_CODE

        file = open( file_path , 'w')

        return NORMAL_CODE

    def writeOfList(self,list):
        if isNull(file):
            echo_open_any_file()
            return ERROR_CODE
        self.writer = csv.writer(file, lineterminator='\n')
        writer.writerow(list)
        return NORMAL_CODE

    def writeOfArray2d(self,array_2d):
        if isNull(file):
            echo_open_any_file()
            return ERROR_CODE
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(array_2d)
        return NORMAL_CODE

class CsvReader():

    def __init__(self):
        self.data      = [[]]

    def readFile(self,file_path):
        if isNull(file_path):
            print(" input file_name ")
            return ERROR_CODE

        if not os.path.exists(file_path):
            print(" do not exist that file " + file_path)
            return ERROR_CODE

        self.file = open( file_path , 'r')
        self.data_list = csv.reader(self.file)
        for self.data_tmp in self.data_list:
            self.data_str_tmp = str(self.data_tmp)
            self.data.append(self.data_str_tmp.split(","))

        del self.data[0]

        return NORMAL_CODE

    def get_data(self):
        return self.data

class CsvReaderViaNp():

    #def __init__(self):
        

    def readFile(self,file_path):
        if isNull(file_path):
            print(" input file_name ")
            return ERROR_CODE

        if not os.path.exists(file_path):
            print(" do not exist that file " + file_path)
            return ERROR_CODE

        self.data = np.genfromtxt(file_path,dtype = None,delimiter=",")
        return NORMAL_CODE

    def get_data(self):
        return self.data

###########################################################
#
# messages
#
###########################################################
def echo_open_any_file():
    print(" open any file ")



