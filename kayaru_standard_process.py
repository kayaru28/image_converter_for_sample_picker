import csv
import os
import sys
import numpy as np
import pandas as pd
import datetime
from time import sleep

ERROR_CODE  = 100
NORMAL_CODE = 0

def exec_sleep(sec):
    sleep(sec)


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

def cut_str_before_key(key,str):
    no  = patternMatch(key,str)
    ans = left( str , no - 1) 
    return ans

def cut_str_after_key(key,str):
    no  = patternMatch(key,str)
    no  = no + ( len(key) - 1 )
    ans = right( str , len(str) - no )
    return ans

def pattern_match(key,str):
    # 一致する　：＞0
    # 一致しない：＝0
    ans = str.find(key) + 1
    return ans

def judge_error(exit_code):
    if exit_code == ERROR_CODE:
        print("!!!!ERROR OCCURED!!!!11!!")
        sys.exit()

def get_script_dir():
    return os.path.abspath(os.path.dirname(__file__))

def get_yyyymmdd():
    return datetime.date.today()

def get_yyyymmddhhmmss():
    return datetime.datetime.now()



###########################################################
#
# varidation
#
###########################################################

def is_not_null(str):
    ans = True

    if(str == None):
        ans = False
    elif(str == ""):
        ans = False
    return ans

def is_null(str):
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

class csvWriter():
    def __init__(self):
        self.file = ""

    def open_file(self,file_path):
        if is_null(file_path):
            echo_null_of_a_value(file_path,locals())
            return ERROR_CODE

        self.file = open( file_path , 'w')

        return NORMAL_CODE

    def close_file(self):
        if is_null(self.file):
            echo_open_any_file()
            return ERROR_CODE

        self.file.close()

    def write_of_val(self,val):
        if is_null(self.file):
            echo_open_any_file()
            return ERROR_CODE
        self.val_list = []
        self.val_list.append(val)
        self.writer = csv.writer(self.file, lineterminator='\n')
        self.writer.writerow(self.val_list)
        return NORMAL_CODE

    def write_of_list(self,list):
        if is_null(self.file):
            echo_open_any_file()
            return ERROR_CODE
        self.writer = csv.writer(self.file, lineterminator='\n')
        self.writer.writerow(list)
        return NORMAL_CODE

    def write_of_array2d(self,array_2d):
        if is_null(self.file):
            echo_open_any_file()
            return ERROR_CODE
        self.writer = csv.writer(self.file, lineterminator='\n')
        self.writer.writerows(array_2d)
        return NORMAL_CODE

class csvReader():

    def __init__(self):
        self.data      = [[]]

    def read_file(self,file_path):
        if is_null(file_path):
            echo_null_of_a_value(file_path,locals())
            return ERROR_CODE

        if not os.path.exists(file_path):
            echo_not_exist_that_file(file_path)
            return ERROR_CODE

        self.file      = open( file_path , 'r')
        self.data_list = csv.reader(self.file)

        for self.data_tmp in self.data_list:
            self.data_str_tmp = str(self.data_tmp)
            self.data.append(self.data_str_tmp.split(","))

        del self.data[0]

        return NORMAL_CODE

    def get_data(self):
        return self.data

class csvReaderViaNp():

    #def __init__(self):
        

    def read_file(self,file_path):
        if is_null(file_path):
            echo_null_of_a_value(file_path,locals())
            return ERROR_CODE

        if not os.path.exists(file_path):
            echo_not_exist_that_file(file_path)
            return ERROR_CODE

        self.data = np.genfromtxt(file_path,dtype=None,delimiter=",")
        return NORMAL_CODE

    def get_data(self):
        return self.data

def get_var_name( var, symboltable=locals(), error=None ) :
    """
    Return a var's name as a string.\nThis funciton require a symboltable(returned value of globals() or locals()) in the name space where you search the var's name.\nIf you set error='exception', this raise a ValueError when the searching failed.
    """
    print("val:" + var)
    for key in symboltable.keys():
        print(key)
        if id(symboltable[key]) == id(var) :
            return key
    else :
        if error == "exception" :
            raise ValueError("Undefined function is mixed in subspace?")
        else:
            return error
    return "error"

def compare_type(val1,val2):
    if type(val1) == type(val2):
        return True
    else:
        return False

###########################################################
#
# messages
#
###########################################################
def echo_open_any_file():
    print(" open any file ")

def echo_not_exist_that_file(file_path):
    print(" not exist that file :" + file_path)

def echo_null_of_a_value(var,symboltable=locals()):
    print(" a value is null :" + get_var_name(var,symboltable) )

def echo_blank():
    print("")

def echo_start(process=""):
    print(str(get_yyyymmddhhmmss()) + "\t start process " + process)
