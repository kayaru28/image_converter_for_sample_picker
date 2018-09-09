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


def clearImagePath(image_path):
    ans = image_path
    clear_word = "["
    ans = kstd.convA2BinWord(ans,clear_word,"")
    clear_word = "]"
    ans = kstd.convA2BinWord(ans,clear_word,"")
    clear_word = "'"
    ans = kstd.convA2BinWord(ans,clear_word,"")
    return ans

class SamplePicker():

    def __init__(self):
        self.name_list_of_image = ""
        self.picking_size       = ""
        
        self.index_0            = 0
    """
    def set_picking_size(self,picking_size):
        # validation
        if not ( kstd.isInt(picking_size) ):
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
        error_handler.assertionCheckIsInt(picking_size,"picking_size")
        error_handler.assertionCheckIsList(name_list,"name_list")

        self.size       = len(name_list)
        self.index_end  = self.size - 1
        self.image_list = []

        for pi in range(picking_size):
            self.index               = rand.getVarInt(self.index_0,self.index_end)
            self.image_file_path     = name_list[self.index]
            self.gray_image_var_d2   = image.convGrayImage2NpList(self.image_file_path)
            self.gray_image_var_nplist = image.convImageNpList2d2Flat(self.gray_image_var_d2)
            self.image_list.append(self.gray_image_var_nplist)

        return self.image_list

def readNameList(name_list_path):
    name_list_file = kstd.CsvReader()
    name_list_file.openFile(name_list_path)
    name_list_file.readFile()
    name_list_row = name_list_file.getData()
    name_list_file.closeFile() 

    name_list = []
    for row in name_list_row:
        name = clearImagePath(row[0])
        name_list.append(name)

    return name_list

if __name__ == "__main__":

    kstd.echoBlank()
    kstd.echoBar()
    kstd.echoBlank()
    
    test_path = "C:\\Users\\istor\\Desktop\\work\\Git\\004_sample_picker\\sample_picker\\_name_list_2018-09-08_no-00.csv"
    picking_size = 10

    name_list     = readNameList(test_path)
    sample_picker = SamplePicker()
    image_list    = sample_picker.sampling(picking_size,name_list)
    kstd.echoList1d(image_list)


    kstd.echoBar()
    kstd.echoBlank()
    print("finished!!!!!!!!!!111!!!!!!!!")



