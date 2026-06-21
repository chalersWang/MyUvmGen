#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import openpyxl
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from common_lib.common_lib import ExtractArray
from common_lib.common_lib import PrintArray
from common_lib.parameters import Parameters

class readexcel_DutSignal_v02:

    def __init__(self):
        print("[readexcel_DutSignal]:initiail")
        EnvironmentGenCfg='../VerifyEnvironmentGenCfg.xlsx'
        self.readexcel_DutSignal_v02_info(EnvironmentGenCfg,PrintEnable=True)

    def readexcel_DutSignal_v02_info(self,EnvironmentGenCfg,PrintEnable):

        wb = openpyxl.load_workbook(EnvironmentGenCfg)
        sheet=wb['DUT_signals']
        self.DUT_Name               =sheet['A2']
        self.DUT_GroupName_sheet    =sheet['B']
        self.DUT_Signals_sheet      =sheet['C']
        self.DUT_InOutType_sheet    =sheet['D']
        self.DUT_Width_sheet        =sheet['E']
        self.DUT_InitialValue_sheet =sheet['F']
        self.DUT_VIP_sheet          =sheet['G']

        self.DUT_GroupName      =[]
        self.DUT_Signals        =[]
        self.DUT_InOutType      =[]
        self.DUT_Width          =[]
        self.DUT_InitialValue   =[]

        # self.DUT_GroupName  =self.ExtractArray(self.DUT_GroupName_sheet,'GroupName')
        # self.DUT_Signals    =self.ExtractArray(self.DUT_Signals_sheet,'Signals')
        # self.DUT_VIP        =self.ExtractArray(self.DUT_VIP_sheet,'VIP')

        self.DUT_GroupName      =ExtractArray(self,self.DUT_GroupName_sheet,'GroupName')
        self.DUT_Signals        =ExtractArray(self,self.DUT_Signals_sheet,'Signals')
        self.DUT_InOutType      =ExtractArray(self,self.DUT_InOutType_sheet,'InOutType')
        self.DUT_Width          =ExtractArray(self,self.DUT_Width_sheet,'Width')
        self.DUT_InitialValue   =ExtractArray(self,self.DUT_InitialValue_sheet,'InitialValue')
        self.DUT_VIP            =ExtractArray(self,self.DUT_VIP_sheet,'VIP')

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")
            PrintArray(self,self.DUT_GroupName,Parameters.PrintEnable)
            PrintArray(self,self.DUT_Signals,Parameters.PrintEnable)
            PrintArray(self,self.DUT_InOutType,Parameters.PrintEnable)
            PrintArray(self,self.DUT_Width,Parameters.PrintEnable)
            PrintArray(self,self.DUT_InitialValue,Parameters.PrintEnable)
            PrintArray(self,self.DUT_VIP,Parameters.PrintEnable)
        
        #return self.DUT_GroupName
           
    # def ExtractArray(self,sheetname,ExtractKeyword):
    #     ExtractKeywordName=[]
    #     for name in sheetname:
    #         if (not name.value ==None)&(not name.value==ExtractKeyword):
    #             ExtractKeywordName.append(name.value)
    #     return ExtractKeywordName

if __name__ == '__main__':
    gen=readexcel_DutSignal_v02()