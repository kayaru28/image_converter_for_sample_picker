#coding: UTF-8

import kayaru_standard_process as kstd
import kayaru_standard_process_for_image as image
import properties as prop
import glob
import numpy as np
import pandas as pd
import os
import joblib as jl

ERROR_CODE = 100
# parameter

def echoProcessTo(str):
    kstd.echoBlank()
    print("process to " + str)


def getLogMessage(count_dir,count_image_file,base_time_0,base_time_n):
    
    elapsed_time_n     = kstd.getElapsedTime(base_time_n,"s")
    elapsed_time_n_int = int(elapsed_time_n)
    elapsed_time_n_str = "{0:04d}".format(elapsed_time_n_int)
    
    elapsed_time_0   = kstd.getElapsedTime(base_time_0)
    elapsed_time_0_int = int(elapsed_time_0)
    elapsed_time_0_str = "{0:04d}".format(elapsed_time_0_int)


    message = str(kstd.getTimeyyyymmddhhmmss())
    message = message + "\tdir:" + "{0:03d}".format(count_dir)
    message = message + "\tfile:" + "{0:07d}".format(count_image_file)
    message = message + "\t(" + elapsed_time_n_str + " s / " + elapsed_time_0_str + " m)"
    return message

def getSleepMessage(count_dir):
    message = str(kstd.getTimeyyyymmddhhmmss())
    message = message + "\tdir:" + "{0:03d}".format(count_dir)
    message = message + "\tI am sleeping......"
    return message

def getNameListFilePath(dir_number):
    file_dir  = kstd.getScriptDir()
    part_name = str(kstd.getDateyyyymmdd()) + "_no-" + "{0:02d}".format(dir_number) 
    part_name = part_name + ".csv"
    file_name = "_name_list_" + part_name
    file_path = os.path.join(file_dir,file_name)
    return file_path

def execUnitProcessForCreateOutputFile(directory,dir_number):

    prop_values = prop.PropValues()

    csv_writer_name_list  = kstd.CsvWriter()
    name_list_file_path  = getNameListFilePath(dir_number)

    image_file_path_list = glob.glob(directory + '\\*') 

    echoProcessTo(directory)

    csv_writer_name_list.openFile(name_list_file_path)

    for image_file_path in image_file_path_list:
        csv_writer_name_list.writeOfVal(image_file_path)

    csv_writer_name_list.closeFile()


def createOutputFile():

    dto_dir        = prop.DtoDirectories()
    directories    = dto_dir.getList()

    # get image flatten list
    # paralell
    len_di = len(directories)

    result = jl.Parallel(n_jobs=-1)([jl.delayed(execUnitProcessForCreateOutputFile)(directories[di],di) for di in range(len_di)])
    #for di in range(len_di):
    #    execUnitProcessForCreateOutputFile(directories[di],di)


if __name__ == "__main__":

    print("")
    print("")
    print("")

    createOutputFile()

    kstd.echoBlank()
    print("finished!!!!!!!!!!111!!!!!!!!")




