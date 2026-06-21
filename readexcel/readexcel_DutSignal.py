#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import openpyxl
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from common_lib.common_lib import ExtractArray

class readexcel_DutSignal:

    def __init__(self):
        print("[readexcel_DutSignal]:initiail")
        EnvironmentGenCfg='VerifyEnvironmentGenCfg.xlsx'
        self.readexcel_DutSignal_info(EnvironmentGenCfg,PrintEnable=True)

    def readexcel_DutSignal_info(self,EnvironmentGenCfg,PrintEnable):

        wb = openpyxl.load_workbook(EnvironmentGenCfg)
        sheet=wb['DUT']
        self.DUT_Name           =sheet['A2']
        self.DUT_GroupName_sheet=sheet['B']
        self.DUT_Signals_sheet  =sheet['C']
        self.DUT_VIP_sheet      =sheet['D']

        self.DUT_GroupName  =[]
        self.DUT_Signals    =[]

        # self.DUT_GroupName  =self.ExtractArray(self.DUT_GroupName_sheet,'GroupName')
        # self.DUT_Signals    =self.ExtractArray(self.DUT_Signals_sheet,'Signals')
        # self.DUT_VIP        =self.ExtractArray(self.DUT_VIP_sheet,'VIP')

        self.DUT_GroupName  =ExtractArray(self,self.DUT_GroupName_sheet,'GroupName')
        self.DUT_Signals    =ExtractArray(self,self.DUT_Signals_sheet,'Signals')
        self.DUT_VIP        =ExtractArray(self,self.DUT_VIP_sheet,'VIP')

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")
        
        #return self.DUT_GroupName
           
    # def ExtractArray(self,sheetname,ExtractKeyword):
    #     ExtractKeywordName=[]
    #     for name in sheetname:
    #         if (not name.value ==None)&(not name.value==ExtractKeyword):
    #             ExtractKeywordName.append(name.value)
    #     return ExtractKeywordName

if __name__ == '__main__':
    gen=readexcel_DutSignal()