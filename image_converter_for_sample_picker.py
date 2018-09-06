#coding: UTF-8

import kayaru_standard_process as kstd
import kayaru_standard_process_for_image as image
import target_directories as target_dir
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
    csvReader = kstd.csvReaderViaNp()

    EXIT_CODE = csvReader.read_file(file_path)

    kstd.judge_error(EXIT_CODE)

    label_tmp = csvReader.get_data()
    label     = str(label_tmp)
    return label

def echo_process_to(str):
    kstd.echo_blank()
    print("process to " + str)

def get_log_message(count_dir,count_image_file):
    message = str(kstd.get_yyyymmddhhmmss())
    message = message + "\tdir:" + "{0:03d}".format(count_dir)
    message = message + "\tfile:" + "{0:07d}".format(count_image_file)
    return message


def exec_unit_process_for_create_output_file(directory,number):
    
    unit_output = 2
    unit_sleep  = 60 * 0.001

    file_dir         = kstd.get_script_dir()
    part_name        = str(kstd.get_yyyymmdd()) + "_no-" + "{0:02d}".format(number) + ".csv"
    output_file_name = "output_file_" + part_name
    output_file_path = os.path.join(file_dir,output_file_name)
    log_file_name    = "log_file_" + part_name
    print("vut" + log_file_name)
    log_file_path    = os.path.join(file_dir,log_file_name)

    dto_image_list    = image.dtoFlatImageDataNplistForTf()

    csv_writer_output = kstd.csvWriter()

    csv_writer_log    = kstd.csvWriter()
    csv_writer_log.open_file(log_file_path)
        
    # set meta data for dto_image_list
    image_file_path_list = glob.glob(directory + '\\*') 
    image_file_path      = image_file_path_list[0]
    height_0             = image.get_height_from_image(image_file_path)
    wigth_0              = image.get_wight_from_image(image_file_path)

    dto_image_list.firstlization(height_0,wigth_0)
    dto_image_list.val_check()

    echo_process_to(directory)
    image_file_path_list = glob.glob(directory + '\\*') 

    count_image_file = 0
    for image_file_path in image_file_path_list:
        gray_image_val_d2   = image.conv_gray_image_2_npList(image_file_path)
        gray_image_val_list = image.conv_image_nplist2d_2_flat(gray_image_val_d2)
        dto_image_list.add_list(gray_image_val_list)
        count_image_file = count_image_file + 1
        if(count_image_file % unit_output == 0):
            message = get_log_message(number,count_image_file)
            print(message)
            csv_writer_log.write_of_val(message)
            kstd.exec_sleep( unit_sleep )

    csv_writer_log.close_file()

    # write for output files
    csv_writer_output.open_file(output_file_path)
    csv_writer_output.write_of_array2d(dto_image_list.get_list())
    csv_writer_output.close_file()



def create_output_file(output_file_path):

    dto_dir        = target_dir.dtoDirectories()
    directories    = dto_dir.get_list()

    # get image flatten list
    # paralell
    for di in range(len(directories)):
        exec_unit_process_for_create_output_file(directories[di],di)

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




