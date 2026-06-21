#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import openpyxl
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from common_lib.common_lib import ExtractArray

class readexcel_ClockRst:

    def __init__(self):
        EnvironmentGenCfg='VerifyEnvironmentGenCfg.xlsx'
        print("[readexcel_ClockRst]:initiail")
        self.readexcel_ClockRst_info(EnvironmentGenCfg,PrintEnable=True)

    def readexcel_ClockRst_info(self,EnvironmentGenCfg,PrintEnable):

        wb = openpyxl.load_workbook(EnvironmentGenCfg)
        sheet=wb['ClockRst']
        clkname_sheet   =sheet['B']
        clkperiod_sheet =sheet['C']
        mhz_sheet       =sheet['D']
        rstname_sheet   =sheet['F']
        rstrelease_sheet=sheet['G']
        
        # Extract relevant information of Clk
        self.Clk_name   =[]
        self.Clk_period =[]
        self.MHZ        =[]
        # self.Clk_name   =self.ExtractArray(clkname_sheet,'Clk_name')
        # self.Clk_period =self.ExtractArray(clkperiod_sheet,'Period/ns')
        # self.MHZ        =self.ExtractArray(mhz_sheet,'MHZ')
        self.Clk_name   =ExtractArray(self,clkname_sheet    ,'Clk_name')
        self.Clk_period =ExtractArray(self,clkperiod_sheet  ,'Period/ns')
        self.MHZ        =ExtractArray(self,mhz_sheet        ,'MHZ')

        # Extract relevant information of Rst
        self.Rst_name   =[]
        self.Rst_release=[]
        # self.Rst_name   =self.ExtractArray(rstname_sheet,'Rst_name')
        # self.Rst_release=self.ExtractArray(rstrelease_sheet,'ReleaseTime/ns')
        self.Rst_name   =ExtractArray(self,rstname_sheet    ,'Rst_name')
        self.Rst_release=ExtractArray(self,rstrelease_sheet ,'ReleaseTime/ns')

        if PrintEnable==True:
            ClkName     ='Clk_name'
            Period      ='Period/ns'
            MHZ         ='MHZ'
            RstName     ='Rst_name'
            ReleaseTime ='ReleaseTime/ns'
            # Clk information
            print(" ------------------------------------")
            print("|  %-5s  |  %-5s  |  %-5s  |"%(ClkName,Period,MHZ))
            print(" ------------------------------------")
            for i in range(len(self.Clk_name)):
                ClkName =self.Clk_name[i]
                Period  =self.Clk_period[i]
                MHZ     =self.Clk_name[i]
                print("  %-10s   %-10s   %-10s"%(ClkName,Period,MHZ))
            # Rst information
            print(" -------------------------------")
            print("|  %-5s  |  %-5s  |"%(RstName,ReleaseTime))
            print(" -------------------------------")
            for i in range(len(self.Rst_name)):
                RstName     =self.Rst_name[i]
                ReleaseTime =self.Rst_release[i]
                print("  %-10s   %-10s"%(RstName,ReleaseTime))

    # def ExtractArray(self,sheetname,ExtractKeyword):
    #     ExtractKeywordName=[]
    #     for name in sheetname:
    #         if (not name.value ==None)&(not name.value==ExtractKeyword):
    #             ExtractKeywordName.append(name.value)
    #     return ExtractKeywordName

if __name__ == '__main__':
    #local_dir='./'
    gen=readexcel_ClockRst()