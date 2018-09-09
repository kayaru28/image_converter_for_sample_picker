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

def echo_process_to(str):
    kstd.echo_blank()
    print("process to " + str)

def get_log_message(count_dir,count_image_file,base_time_0,base_time_n):
    
    elapsed_time_n     = kstd.get_elapsed_time(base_time_n,"s")
    elapsed_time_n_int = int(elapsed_time_n)
    elapsed_time_n_str = "{0:04d}".format(elapsed_time_n_int)
    
    elapsed_time_0   = kstd.get_elapsed_time(base_time_0)
    elapsed_time_0_int = int(elapsed_time_0)
    elapsed_time_0_str = "{0:04d}".format(elapsed_time_0_int)


    message = str(kstd.get_yyyymmddhhmmss())
    message = message + "\tdir:" + "{0:03d}".format(count_dir)
    message = message + "\tfile:" + "{0:07d}".format(count_image_file)
    message = message + "\t(" + elapsed_time_n_str + " s / " + elapsed_time_0_str + " m)"
    return message

def get_sleep_message(count_dir):
    message = str(kstd.get_yyyymmddhhmmss())
    message = message + "\tdir:" + "{0:03d}".format(count_dir)
    message = message + "\tI am sleeping......"
    return message

def get_name_list_file_path(dir_number):
    file_dir  = kstd.get_script_dir()
    part_name = str(kstd.get_yyyymmdd()) + "_no-" + "{0:02d}".format(dir_number) 
    part_name = part_name + ".csv"
    file_name = "_name_list_" + part_name
    file_path = os.path.join(file_dir,file_name)
    return file_path

def exec_unit_process_for_create_output_file(directory,dir_number):

    prop_values = prop.propValues()

    csv_writer_name_list  = kstd.csvWriter()
    name_list_file_path  = get_name_list_file_path(dir_number)

    image_file_path_list = glob.glob(directory + '\\*') 

    echo_process_to(directory)

    csv_writer_name_list.open_file(name_list_file_path)

    for image_file_path in image_file_path_list:
        csv_writer_name_list.write_of_val(image_file_path)

    csv_writer_name_list.close_file()


def create_output_file():

    dto_dir        = prop.dtoDirectories()
    directories    = dto_dir.get_list()

    # get image flatten list
    # paralell
    len_di = len(directories)

    result = jl.Parallel(n_jobs=-1)([jl.delayed(exec_unit_process_for_create_output_file)(directories[di],di) for di in range(len_di)])
    #for di in range(len_di):
    #    exec_unit_process_for_create_output_file(directories[di],di)


if __name__ == "__main__":

    print("")
    print("")
    print("")

    create_output_file()

    kstd.echo_blank()
    print("finished!!!!!!!!!!111!!!!!!!!")




