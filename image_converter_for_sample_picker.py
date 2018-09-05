#coding: UTF-8

import kayaru_standard_process as kstd
import glob
import numpy as np
import pandas as pd
import os

ERROR_CODE = 100
# parameter

def read_label():
    dim_label = 0
    file_dir  = kstd.get_script_dir()
    file_path = file_dir + "/label.csv"
    csvReader = kstd.CsvReaderViaNp()
    EXIT_CODE = csvReader.readFile(file_path)
    kstd.judgeError(EXIT_CODE)

    label_tmp = csvReader.get_data()
    label     = str(label_tmp)
    return label

def read_target_directories():
    dim_dir   = 0
    file_dir  = kstd.get_script_dir()
    file_path = file_dir + "/directories.csv"
    csvReader = kstd.CsvReaderViaNp()
    EXIT_CODE = csvReader.readFile(file_path)
    kstd.judgeError(EXIT_CODE)

    dir_list  = csvReader.get_data()
    return dir_list

def echo_process_to(str):
    print("process to " + str)
    print("")


if __name__ == "__main__":

    print("")
    print("")
    print("")

    label       = read_label()

    output_file_dir  = kstd.get_script_dir()
    output_file_name = "image_label" + label + ".csv"
    output_file_path = os.path.join(output_file_dir,output_file_name)

    csvWriter = kstd.CsvWriter()


    directories = read_target_directories()
    for directory_i in directories:
        directory = str(directory_i)
        echo_process_to(directory)
        image_files = glob.glob(directory + '\\*') 

        for image_file in image_files:
            gray_image = np.array(Image.open(image_file).convert('L'))
            print(gray_image)
