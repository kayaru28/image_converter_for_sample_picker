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


class DtoPickeredSample():
    def __init__(self):
        self.sample_list = []
        self.label_list = []
        
    def firstlization(self):
        self.sample_list = []
        self.label_list  = []

    def addLists(self,sample_list,label_list):
        self.sample_list.extend(sample_list)
        self.label_list.extend(label_list)

    def getSampleList(self):
        return self.sample_list

    def getLabelList(self):
        return self.label_list

class SamplePicker():

    def __init__(self):
        self.name_list_of_image  = ""
        self.picking_size        = ""
        
        self.index_0             = 0
        self.dto_pickered_sample = DtoPickeredSample()
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

    def sampling(self,dto_pickered_sample,picking_size,name_list,label):

        # validation for parameters
        error_handler.assertionCheckIsInt(picking_size,"picking_size")
        error_handler.assertionCheckIsList(name_list,"name_list")

        self.size       = len(name_list)
        self.index_end  = self.size - 1
        self.image_list = []
        self.label_list = []
        self.posi_label = 1
        self.nega_label = 0

        if label == self.posi_label:
            self.unit_label = [1,0]
        elif label == self.nega_label:
            self.unit_label = [0,1]
        else:
            error_handler.assertionCheck(False,"settinglabel is wrong")

        for pi in range(picking_size):
            self.index                 = rand.getVarInt(self.index_0,self.index_end)
            self.image_file_path       = name_list[self.index]
            self.gray_image_var_d2     = image.convGrayImage2NpList(self.image_file_path)
            self.gray_image_var_nplist = image.convImageNpList2d2Flat(self.gray_image_var_d2)
            self.image_list.append(self.gray_image_var_nplist)
            self.label_list.append(self.unit_label)

        error_handler.assertionCheckIsList(self.image_list,"image_list in sample picker")
        error_handler.assertionCheckIsList(self.label_list,"label_list in sample picker")

        dto_pickered_sample.addLists(self.image_list,self.label_list)

        return kstd.NORMAL_CODE

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
    
    test_path = "C:\\Users\\istor\\Desktop\\work\\102_DSL_cyclone_classification\\name_list\\_nonTC_00.csv"
    picking_size = 10

    name_list     = readNameList(test_path)
    sample_picker = SamplePicker()

    dto_pickered_sample = DtoPickeredSample()
    label = 1
    sample_picker.sampling(dto_pickered_sample,picking_size,name_list,label)

    kstd.echoBar()
    kstd.echoBlank()
    print("finished!!!!!!!!!!111!!!!!!!!")



