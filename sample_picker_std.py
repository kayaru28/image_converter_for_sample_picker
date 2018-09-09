#coding: UTF-8

import kayaru_standard_process as kstd
import kayaru_standard_process_for_image as image
import kayaru_standard_process_for_randomize as rand
import kayaru_standard_process_for_error_handling as error_handler
import kayaru_standard_messages as kstd_m
import glob
import numpy as np
import pandas as pd
import os
import joblib as jl


def clear_image_path(image_path):
    ans = image_path
    clear_word = "["
    ans = kstd.conv_a_to_b_in_word(ans,clear_word,"")
    clear_word = "]"
    ans = kstd.conv_a_to_b_in_word(ans,clear_word,"")
    clear_word = "'"
    ans = kstd.conv_a_to_b_in_word(ans,clear_word,"")
    return ans

class samplePicker():

    def __init__(self):
        self.name_list_of_image = ""
        self.picking_size       = ""
        
        self.index_0            = 0
    """
    def set_picking_size(self,picking_size):
        # validation
        if not ( kstd.is_int(picking_size) ):
            self.name    = "picking_size"
            self.message = kstd_m.get_X_is_not_int(self.name)
            kstd.echo_error_occured(self.message)
            self.picking_size = ""

        # processing start
        self.picking_size = picking_size

    def set_name_list_of_image(self,name_list):
        self.name_list_of_image = name_list
    """

    def sampling(self,picking_size,name_list):

        # validation for parameters
        error_handler.assertion_check_is_int(picking_size,"picking_size")
        error_handler.assertion_check_is_list(name_list,"name_list")

        self.size       = len(name_list)
        self.index_end  = self.size - 1
        self.image_list = []

        for pi in range(picking_size):
            self.index               = rand.get_var_int(self.index_0,self.index_end)
            self.image_file_path     = name_list[self.index]
            self.gray_image_var_d2   = image.conv_gray_image_2_npList(self.image_file_path)
            self.gray_image_var_nplist = image.conv_image_nplist2d_2_flat(self.gray_image_var_d2)
            self.image_list.append(self.gray_image_var_nplist)

        return self.image_list

def read_name_list(name_list_path):
    name_list_file = kstd.csvReader()
    name_list_file.open_file(name_list_path)
    name_list_file.read_file()
    name_list_row = name_list_file.get_data()
    name_list_file.close_file() 

    name_list = []
    for row in name_list_row:
        name = clear_image_path(row[0])
        name_list.append(name)

    return name_list

if __name__ == "__main__":

    kstd.echo_blank()
    kstd.echo_bar()
    kstd.echo_blank()
    
    test_path = "C:\\Users\\istor\\Desktop\\work\\Git\\004_sample_picker\\sample_picker\\_name_list_2018-09-08_no-00.csv"
    picking_size = 10

    name_list     = read_name_list(test_path)
    sample_picker = samplePicker()
    image_list    = sample_picker.sampling(picking_size,name_list)
    kstd.echo_list1d(image_list)


    kstd.echo_bar()
    kstd.echo_blank()
    print("finished!!!!!!!!!!111!!!!!!!!")



