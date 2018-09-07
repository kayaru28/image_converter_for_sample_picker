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

def read_label():
    dim_label = 0
    file_dir  = kstd.get_script_dir()
    file_path = file_dir + "/label.csv"
    csvReader = kstd.csvReaderViaNp()

    EXIT_CODE = csvReader.read_file(file_path)

    kstd.judge_error(EXIT_CODE)

    label_tmp = csvReader.get_data()
    label     = str(label_tmp)
    return label

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


def get_image_list_file_path(dir_number,output_number):
    file_dir  = kstd.get_script_dir()
    part_name = str(kstd.get_yyyymmdd()) + "_no-" + "{0:02d}".format(dir_number) 
    part_name = part_name + "-" + "{0:02d}".format(output_number) + ".csv"
    file_name = "_image_" + part_name
    file_path = os.path.join(file_dir,file_name)
    return file_path

def get_name_list_file_path(dir_number,output_number):
    file_dir  = kstd.get_script_dir()
    part_name = str(kstd.get_yyyymmdd()) + "_no-" + "{0:02d}".format(dir_number) 
    part_name = part_name + "-" + "{0:02d}".format(output_number) + ".csv"
    file_name = "_name_list_" + part_name
    file_path = os.path.join(file_dir,file_name)
    return file_path

def get_log_file_path(dir_number):
    file_dir  = kstd.get_script_dir()
    file_name = "_log_" + str(kstd.get_yyyymmdd()) + "_no-" + "{0:02d}".format(dir_number) + ".csv"
    file_path = os.path.join(file_dir,file_name)
    return file_path

def exec_unit_process_for_create_output_file(directory,dir_number):

    prop_values = prop.propValues()

    output_number = 1

    csv_writer_image_list = kstd.csvWriter()
    csv_writer_name_list  = kstd.csvWriter()
    csv_writer_log        = kstd.csvWriter()
    
    image_list_file_path = get_image_list_file_path(dir_number,output_number)
    name_list_file_path  = get_name_list_file_path(dir_number,output_number)
    log_file_path        = get_log_file_path(dir_number)

    dto_image_list    = image.dtoFlatImageDataNplistForTf()


    csv_writer_log.open_file(log_file_path)
        
    # set meta data for dto_image_list
    image_file_path_list = glob.glob(directory + '\\*') 
    image_file_path      = image_file_path_list[0]
    height_0             = image.get_height_from_image(image_file_path)
    wigth_0              = image.get_wight_from_image(image_file_path)

    dto_image_list.firstlization(height_0,wigth_0)
    dto_image_list.val_check()

    echo_process_to(directory)

    count_image_file = 0
    csv_writer_image_list.open_file(image_list_file_path)
    csv_writer_name_list.open_file(name_list_file_path)

    base_time_0 = kstd.get_time()
    base_time_n = kstd.get_time()
    for image_file_path in image_file_path_list:

        gray_image_val_d2   = image.conv_gray_image_2_npList(image_file_path)
        gray_image_val_list = image.conv_image_nplist2d_2_flat(gray_image_val_d2)

        dto_image_list.add_list(gray_image_val_list)

        image_file_name = kstd.get_file_name_from_path(image_file_path)
        csv_writer_name_list.write_of_val(image_file_name)

        count_image_file = count_image_file + 1

        if(count_image_file % prop_values.cycle_file == 0):
            csv_writer_image_list.close_file()
            csv_writer_name_list.close_file()

            output_number        = output_number + 1
            image_list_file_path = get_image_list_file_path(dir_number,output_number)
            name_list_file_path  = get_name_list_file_path(dir_number,output_number)
            csv_writer_image_list.open_file(image_list_file_path)
            csv_writer_name_list.open_file(name_list_file_path)

        if(count_image_file % prop_values.cycle_write_image == 0 ):
            csv_writer_image_list.write_of_array2d(dto_image_list.get_list())
            dto_image_list.clear_list()

        if(count_image_file % prop_values.cycle_log == 0):
            message = get_log_message(dir_number,count_image_file,base_time_0,base_time_n)
            print(message)
            csv_writer_log.write_of_val(message)
            base_time_n = kstd.get_time()

        if(count_image_file % prop_values.cycle_sleep == 0):
            message = get_sleep_message(dir_number)
            print(message)
            kstd.exec_sleep( prop_values.time_sleep )
            base_time_n = kstd.get_time()


    csv_writer_image_list.write_of_array2d(dto_image_list.get_list())
    csv_writer_image_list.close_file()
    csv_writer_name_list.close_file()
    csv_writer_log.close_file()


def create_output_file(output_file_path):

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

    label       = read_label()

    output_file_dir  = kstd.get_script_dir()
    output_file_name = "image_list_label" + label + ".csv"
    output_file_path = os.path.join(output_file_dir,output_file_name)
   
    create_output_file(output_file_path)

    kstd.echo_blank()
    print("finished!!!!!!!!!!111!!!!!!!!")




