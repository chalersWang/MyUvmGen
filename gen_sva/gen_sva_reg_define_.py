#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os
import openpyxl
import xlrd
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from common_lib.common_lib import ExtractArray

class gen_sva_reg_definegen_sva_reg_define:

    def __init__(self,EnvironmentGenCfg):
        print("[gen_sva_reg_definegen_sva_reg_define]:initiail")
        if(EnvironmentGenCfg==''):
            EnvironmentGenCfg='VerifyEnvironmentGenCfg.xlsx'
        print(EnvironmentGenCfg)
        self.gen_sva_reg_definegen_sva_reg_define_info(EnvironmentGenCfg,PrintEnable=True)

    def gen_sva_reg_definegen_sva_reg_define_info(self,EnvironmentGenCfg,PrintEnable):
        ModuleName='test'#SPE
        # 加载工作簿
        wb = openpyxl.load_workbook(EnvironmentGenCfg)
        # 选择活动的工作表或者通过名字选择工作表
        ws=wb.active
        # 遍历每一行
        for row in ws.iter_rows():
            print("====")
            print(row)  # row 是一个元组，包含一行的所有单元格的值
            for i in range(len(row)):
                print(row[i])

        sheet=wb['testreg']
        REG_RegAddr_sheet    =sheet['A']
        REG_Name_sheet       =sheet['B']
        REG_Bits_sheet       =sheet['C']
        REG_Filed_sheet      =sheet['D']
        REG_Access_sheet     =sheet['E']
        REG_ResetValue_sheet =sheet['F']
        REG_ResetCtrl_sheet  =sheet['G']
        REG_Description_sheet=sheet['H']

        REG_RegAddr    =[]
        REG_Name       =[]
        REG_Bits       =[]
        REG_Filed_     =[]
        REG_Access     =[]
        REG_ResetValue =[]
        REG_ResetCtrl  =[]
        REG_Description=[]

        REG_RegAddr    =ExtractArray(self,REG_RegAddr_sheet    ,'OffsetAddr')
        REG_Name       =ExtractArray(self,REG_Name_sheet       ,'Register Name')
        REG_Bits       =ExtractArray(self,REG_Bits_sheet       ,'Bits')
        REG_Filed      =ExtractArray(self,REG_Filed_sheet      ,'Field Name')
        REG_Access     =ExtractArray(self,REG_Access_sheet     ,'Access')
        REG_ResetValue =ExtractArray(self,REG_ResetValue_sheet ,'Reset Value')
        REG_ResetCtrl  =ExtractArray(self,REG_ResetCtrl_sheet  ,'Reset Ctrl')
        REG_Description=ExtractArray(self,REG_Description_sheet,'Description')
             
        filename = open("`define_REG_%s.v"%ModuleName, "w+")
        # for i in range(len(self.REG_Name)):
        #     filename.write("`define Reg%s_%s\t\t\t`TX82_CGRA_DV_IT_ADDRMAP_REG_%s+16'h00\n"\
        #                    %(ModuleName.upper(),REG_Name[i],ModuleName))
        for i in range(len(REG_Name)):
            filename.write("`define Reg%s_%s\t\t\t`ADDRMAP_REG_%s+%s\n"\
                           %(ModuleName.upper(),REG_Name[i],ModuleName,REG_RegAddr[i].replace('0x','64\'h')))

        filename.write("\n")
        filename.close()

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")
        
 
if __name__ == '__main__':
    # EnvironmentGenCfg=Parameters.EnvironmentGenCfg
    # judge where there is a VerifyEnvironmentGenCfg file 
    if len(sys.argv) == 1:
        EnvironmentGenCfg = input('Please input excel file name:\n')
    else:
        EnvironmentGenCfg = sys.argv[1]
    # if EnvironmentGenCfg.strip() == '':
    #     print("\nError: No excel file name provided !!!")
    #     print("Program terminated ...")
    #     time.sleep(3)
    #     raise Exception("No excel file name provided !!!")
    # if not os.path.exists(EnvironmentGenCfg):
    #     print("\nError: No excel file name provided !!!")
    #     print("Program terminated ...")
    #     time.sleep(3)
    #     raise Exception("No excel file name provided !!!")
    gen=gen_sva_reg_definegen_sva_reg_define(EnvironmentGenCfg)