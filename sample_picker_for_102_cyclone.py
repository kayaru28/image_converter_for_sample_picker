#coding: UTF-8

import kayaru_standard_process as kstd
import sample_picker_std       as sp_std
import properties_102_cyclone  as prop


import kayaru_standard_process_for_image as image
import kayaru_standard_process_for_randomize as rand
import kayaru_standard_process_for_error_handling as error_handler
import kayaru_standard_messages as kstd_m
import glob
import numpy as np
import pandas as pd
import os
import joblib as jl


def getNameOfPosiNameList(number):
    return "_TC_{0:02d}.csv".format(number)

def getNameOfNegaNameList(number):
    return "_nonTC_{0:02d}.csv".format(number)


def getPosiRate():
    rand_min           = int( prop.posi_rate_min * 10 )
    rand_max           = int( prop.posi_rate_max * 10 )
    rand_for_posi_rate = rand.getVarInt(rand_min,rand_max)
    posi_rate          = float(rand_for_posi_rate) / 10
    return posi_rate


def getNegaImageList(dto_pickered_sample,nega_sample_size):

    label = 0

    kstd.echoStart("negative image sampling")
    
    unit_nega_sample_size = int ( nega_sample_size / prop.nega_list_total ) + 1

    sample_picker       = sp_std.SamplePicker()

    for ni in range(prop.nega_list_total):

        file_dir       = prop.dir_of_name_list_file
        file_name      = getNameOfNegaNameList(ni)
        name_list_path = os.path.join(file_dir,file_name)
        name_list      = sp_std.readNameList(name_list_path)
        sample_picker.sampling(dto_pickered_sample,unit_nega_sample_size,name_list,label)

    return kstd.NORMAL_CODE

def getPosiImageList(dto_pickered_sample,posi_sample_size):

    label = 1

    kstd.echoStart("positive image sampling")

    sample_picker       = sp_std.SamplePicker()

    file_dir       = prop.dir_of_name_list_file
    file_name      = getNameOfPosiNameList(0)
    name_list_path = os.path.join(file_dir,file_name)
    name_list      = sp_std.readNameList(name_list_path)

    sample_picker.sampling(dto_pickered_sample,posi_sample_size,name_list,label)
    
    return kstd.NORMAL_CODE   

if __name__ == "__main__":

    kstd.echoBlank()
    kstd.echoBar()
    kstd.echoBlank()
    
    posi_rate = getPosiRate()
    posi_sample_size = int( prop.sample_size * posi_rate )
    nega_sample_size = int( prop.sample_size * ( 1 - posi_rate ) )

    dto_pickered_sample     = sp_std.DtoPickeredSample()

    # nega sample picking
    getNegaImageList(dto_pickered_sample,nega_sample_size)
    kstd.echoBar()
    kstd.echoBar()
    print(dto_pickered_sample.getLabelList())    


    # posi sample picking
    getPosiImageList(dto_pickered_sample,posi_sample_size)

    sample_list = dto_pickered_sample.getSampleList()
    label_list  = dto_pickered_sample.getLabelList()
    
    kstd.echoList1d(sample_list)
    kstd.echoList1d(label_list)

    kstd.echoBlank()
    kstd.echoBar()
    kstd.echoBlank()
    print("finished!!!!!!!!!!111!!!!!!!!")



