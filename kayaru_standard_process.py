import csv
import os
import sys
import numpy as np
import pandas as pd
import datetime
import time
import inspect

ERROR_CODE  = 100
NORMAL_CODE = 0

def exec_sleep(sec):
    time.sleep(sec)

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

def conv_a_to_b_in_word(word,a,b):
    ans = word.replace(a, b) 
    return ans

def get_script_dir():
    return os.path.abspath(os.path.dirname(__file__))

def get_file_name_from_path(file_path):
    return os.path.basename(file_path)

def get_yyyymmdd():
    return str(datetime.date.today())

def get_yyyymmddhhmmss():
    return str(datetime.datetime.now())

def get_time():
    return time.time()

def get_elapsed_time(base_time,unit="m"):
    elapsed_time = time.time() - base_time
    if unit == "m":
        elapsed_time = elapsed_time / 60
    elif unit == "h":
        elapsed_time = elapsed_time / 60 / 60
    return elapsed_time

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

def is_int(val):
    if type(val) is int:
        return True
    else:
        return False

def is_str(val):
    if type(val) is str:
        return True
    else:
        return False

def is_tuple(target):
    if isinstance(target, tuple):
        return True
    else:
        return False

def is_list(target):
    if isinstance(target, list):
        return True
    else:
        return False

def is_even_number(val):

    if not type(val) is int:
        return False
    elif ( val % 2 == 0 ):
        return True
    else:
        return False

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

    def open_file_for_add(self,file_path):
        if is_null(file_path):
            echo_null_of_a_value(file_path,locals())
            return ERROR_CODE
        if not os.path.exists(file_path):
            echo_not_exist_that_file(file_path)
            return ERROR_CODE

        self.file = open( file_path , 'a')

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
        self.file = ""
        self.data      = [[]]

    def open_file(self,file_path):
        if is_null(file_path):
            echo_null_of_a_value(file_path,locals())
            return ERROR_CODE

        if not os.path.exists(file_path):
            echo_not_exist_that_file(file_path)
            return ERROR_CODE

        self.file = open( file_path , "r")

        return NORMAL_CODE

    def close_file(self):
        if is_null(self.file):
            echo_open_any_file()
            return ERROR_CODE

        self.file.close()

    def read_file(self):

        if is_null(self.file):
            echo_open_any_file()
            return ERROR_CODE

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
        if is_null(self.file):
            echo_open_any_file()
            return ERROR_CODE

        self.data = np.genfromtxt(file_path,dtype=None,delimiter=",")
        return NORMAL_CODE

    def get_data(self):
        return self.data


def get_var_name( var, symboltable=locals(), error=None ) :
    ans = "("
    for key in symboltable.keys():
        # in consideration of exsisting paires of same id variable
        if id(symboltable[key]) == id(var) :
            ans = ans + " "  + key
    ans = ans + " )"
    return ans

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

#### layer 1 messages

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

def echo_bar(length="50",mark="*"):
    
    if not (is_int(length)):
        length = 50

    bar = ""
    for i in range(length):
        bar = bar + mark
    print(bar)

#### layer 2 messages

def echo_error_occured(detail=""):
    echo_blank()
    echo_bar()
    print("error is occured !!!!!!!!")
    if(detail!=""):
        print("\t(detail) " + detail)
    echo_bar()
    echo_blank()


