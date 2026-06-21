#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import openpyxl
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from common_lib.common_lib import ExtractArray

class readexcel_RegMem:

    def __init__(self):
        print("[readexcel_RegMem]:initiail")
        EnvironmentGenCfg='VerifyEnvironmentGenCfg.xlsx'
        self.readexcel_RegMem_info(EnvironmentGenCfg,PrintEnable=True)

    def readexcel_RegMem_info(self,EnvironmentGenCfg,PrintEnable):

        wb = openpyxl.load_workbook(EnvironmentGenCfg)
        # sheet=wb['RegModel']
        # sheet=wb['testreg']
        sheet=wb['RegModel']
        self.REG_Name_sheet       =sheet['A']
        self.REG_Bits_sheet       =sheet['B']
        self.REG_Filed_sheet      =sheet['C']
        self.REG_Access_sheet     =sheet['D']
        self.REG_ResetValue_sheet =sheet['E']
        self.REG_ResetCtrl_sheet  =sheet['F']
        self.REG_Description_sheet=sheet['G']

        self.REG_Name       =[]
        self.REG_Bits       =[]
        self.REG_Filed_     =[]
        self.REG_Access     =[]
        self.REG_ResetValue =[]
        self.REG_ResetCtrl  =[]
        self.REG_Description=[]

        self.REG_Name       =ExtractArray(self,self.REG_Name_sheet       ,'Register Name')
        self.REG_Bits       =ExtractArray(self,self.REG_Bits_sheet       ,'Bits')
        self.REG_Filed      =ExtractArray(self,self.REG_Filed_sheet      ,'Field Name')
        self.REG_Access     =ExtractArray(self,self.REG_Access_sheet     ,'Access')
        self.REG_ResetValue =ExtractArray(self,self.REG_ResetValue_sheet ,'Reset Value')
        self.REG_ResetCtrl  =ExtractArray(self,self.REG_ResetCtrl_sheet  ,'Reset Ctrl')
        self.REG_Description=ExtractArray(self,self.REG_Description_sheet,'Description')

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")
            print("========================================================")
            print(len(self.REG_Name))
            for i in range(len(self.REG_Name)):
                print(self.REG_Name[i])
            print("========================================================")
            print(len(self.REG_Bits))
            for i in range(len(self.REG_Bits)):
                print(self.REG_Bits[i])
            print("========================================================")
            print(len(self.REG_Filed))
            for i in range(len(self.REG_Filed)):
                print(self.REG_Filed[i])
            print("========================================================")
            print(len(self.REG_Access))
            for i in range(len(self.REG_Access)):
                print(self.REG_Access[i])
            print("========================================================")
            print(len(self.REG_ResetValue))
            for i in range(len(self.REG_ResetValue)):
                print(self.REG_ResetValue[i])
            print("========================================================")
            print(len(self.REG_ResetCtrl))
            for i in range(len(self.REG_ResetCtrl)):
                print(self.REG_Name[i])
            print("========================================================")
            print(len(self.REG_Description))
            for i in range(len(self.REG_Description)):
                print(self.REG_Description[i])

if __name__ == '__main__':
    gen=readexcel_RegMem()