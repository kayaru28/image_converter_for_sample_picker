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


def getImageListFilePath(dir_number,output_number):
    file_dir  = kstd.getScriptDir()
    part_name = str(kstd.getDateyyyymmdd()) + "_no-" + "{0:02d}".format(dir_number) 
    part_name = part_name + "-" + "{0:02d}".format(output_number) + ".csv"
    file_name = "_image_" + part_name
    file_path = os.path.join(file_dir,file_name)
    return file_path

def getNameListFilePath(dir_number,output_number):
    file_dir  = kstd.getScriptDir()
    part_name = str(kstd.getDateyyyymmdd()) + "_no-" + "{0:02d}".format(dir_number) 
    part_name = part_name + "-" + "{0:02d}".format(output_number) + ".csv"
    file_name = "_name_list_" + part_name
    file_path = os.path.join(file_dir,file_name)
    return file_path

def getLogFilePath(dir_number):
    file_dir  = kstd.getScriptDir()
    file_name = "_log_" + str(kstd.getDateyyyymmdd()) + "_no-" + "{0:02d}".format(dir_number) + ".csv"
    file_path = os.path.join(file_dir,file_name)
    return file_path

def execUnitProcessForCreateOutputFile(directory,dir_number):

    prop_values = prop.PropValues()

    output_number = 1

    csv_writer_image_list = kstd.CsvWriter()
    csv_writer_name_list  = kstd.CsvWriter()
    csv_writer_log        = kstd.CsvWriter()
    
    image_list_file_path = getImageListFilePath(dir_number,output_number)
    name_list_file_path  = getNameListFilePath(dir_number,output_number)
    log_file_path        = getLogFilePath(dir_number)

    dto_image_list    = image.DtoFlatImageDataNplistForTf()


    csv_writer_log.openFile(log_file_path)
        
    # set meta data for dto_image_list
    image_file_path_list = glob.glob(directory + '\\*') 
    image_file_path      = image_file_path_list[0]
    height_0             = image.getHeightFromImage(image_file_path)
    wigth_0              = image.getWightFromImage(image_file_path)

    dto_image_list.firstlization(height_0,wigth_0)
    dto_image_list.valCheck()

    echoProcessTo(directory)

    count_image_file = 0
    csv_writer_image_list.openFile(image_list_file_path)
    csv_writer_name_list.openFile(name_list_file_path)

    base_time_0 = kstd.getTime()
    base_time_n = kstd.getTime()
    for image_file_path in image_file_path_list:

        gray_image_val_d2   = image.convGrayImage2NpList(image_file_path)
        gray_image_val_list = image.convImageNpList2d2Flat(gray_image_val_d2)

        dto_image_list.addList(gray_image_val_list)

        image_file_name = kstd.getFileNameFromPath(image_file_path)
        csv_writer_name_list.writeOfVal(image_file_name)

        count_image_file = count_image_file + 1

        if(count_image_file % prop_values.cycle_file == 0):
            csv_writer_image_list.closeFile()
            csv_writer_name_list.closeFile()

            output_number        = output_number + 1
            image_list_file_path = getImageListFilePath(dir_number,output_number)
            name_list_file_path  = getNameListFilePath(dir_number,output_number)
            csv_writer_image_list.openFile(image_list_file_path)
            csv_writer_name_list.openFile(name_list_file_path)

        if(count_image_file % prop_values.cycle_write_image == 0 ):
            csv_writer_image_list.writeOfArray2d(dto_image_list.get_list())
            dto_image_list.clearList()

        if(count_image_file % prop_values.cycle_log == 0):
            message = getLogMessage(dir_number,count_image_file,base_time_0,base_time_n)
            print(message)
            csv_writer_log.writeOfVal(message)
            base_time_n = kstd.getTime()

        if(count_image_file % prop_values.cycle_sleep == 0):
            message = getSleepMessage(dir_number)
            print(message)
            kstd.execSleep( prop_values.time_sleep )
            base_time_n = kstd.getTime()


    csv_writer_image_list.writeOfArray2d(dto_image_list.getList())
    csv_writer_image_list.closeFile()
    csv_writer_name_list.closeFile()
    csv_writer_log.closeFile()


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




