#coding: UTF-8

import kayaru_standard_process as kstd
import numpy as np
import pandas as pd
import os
ERROR_CODE = 100
# parameter

def read_label():
    label     = ""
    file_dir  = os.path.abspath(os.path.dirname(__file__)) 
    file_path = file_dir + "/label.csv"
    csvReader = kstd.CsvReader()
    EXIT_CODE = csvReader.readFile(file_path)
    kstd.judgeError(EXIT_CODE)

    label     = csvReader.get_data()
    return label

if __name__ == "__main__":

    label = read_label()
    print(label)
        






