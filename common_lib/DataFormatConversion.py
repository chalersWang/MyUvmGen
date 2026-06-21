#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os
import sys
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

class DataFormatConversion:

    def __init__(self):
        print("[DataFormatConversion]:initial")
        FilePath    ='data.pat'
        EndianMode  ='LittleEndian'#BigEndian
        StartStrNum =10
        LineGroup=[4,8]
        InputFormat ='hex'  #'bin','oct','int','hex'
        OutputFormat='hex'  #'bin','oct','int','hex'
        self.DataFormatConversion(FilePath,EndianMode,StartStrNum,LineGroup,InputFormat,OutputFormat,True)

    def DataFormatConversion(self,FilePath,EndianMode,StartStrNum,LineGroup,InputFormat,OutputFormat,PrintEnable):
        
        # with open(FilePath,'r') as f:
        #     lines=f.readlines()
        #     for i in range(len(lines)):
        #         #print(lines[i])
        #         line=lines[i].replace(" ","")
        #         for j in range(len(line)):
        #             if j>=StartStrNum:
        #                 print(line[j])

        with open(FilePath,'r') as f:
            lines=f.readline()
            data_array=[]
            while lines:
                num=list(map(str,lines.split(' ')))
                data_array.append(num)
                lines=f.readline()
            data_array=np.array(data_array)
        
        #print(data_array)
        for i in range(len(data_array)):
            print(data_array[i])

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")

            
if __name__ == '__main__':
    gen=DataFormatConversion()