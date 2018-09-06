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

def create_output_file(output_file_path):

    dto_dir        = target_dir.dtoDirectories()
    dto_image_list = image.dtoFlatImageDataNplistForTf()
    
    csv_writer     = kstd.csvWriter()
    directories    = dto_dir.get_list()
    
    # set meta data for dto_image_list
    directory            = directories[0]
    image_file_path_list = glob.glob(directory + '\\*') 
    image_file_path      = image_file_path_list[0]
    height_0             = image.get_height_from_image(image_file_path)
    wigth_0              = image.get_wight_from_image(image_file_path)

    dto_image_list.firstlization(height_0,wigth_0)
    dto_image_list.val_check()

    # get image flatten list
    for directory in directories:
        echo_process_to(directory)
        image_file_path_list = glob.glob(directory + '\\*') 

        for image_file_path in image_file_path_list:
            gray_image_val_d2   = image.conv_gray_image_2_npList(image_file_path)
            gray_image_val_list = image.conv_image_nplist2d_2_flat(gray_image_val_d2)
            dto_image_list.add_list(gray_image_val_list)

    # write for output files
    csv_writer.open_file(output_file_path)
    csv_writer.write_of_array2d(dto_image_list.get_list())


if __name__ == "__main__":

    print("")
    print("")
    print("")

    label       = read_label()

    output_file_dir  = kstd.get_script_dir()
    output_file_name = "image_list_label" + label + ".csv"
    output_file_path = os.path.join(output_file_dir,output_file_name)

    echo_process_to(output_file_name)
    
    create_output_file(output_file_path)

    kstd.echo_blank()
    print("finished!!!!!!!!!!111!!!!!!!!")




