#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os
import sys
import openpyxl
import json
import re
import argparse

#sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

#=======================================================================
initial_vseqr       ='wxx_vseqr'
initial_excel_name  = "./VerifyPlan.xlsx"
initial_sheet_name  = "CaseList"
initial_wave_path   = "$VERIFY_HOME/tcl/wave.tcl"
#=======================================================================
class excel_to_json:

    def __init__(self):
        print("[excel_to_json]:initiail")
        self.json_name =[]
        self.json_strstr=[]
        self.GetArgs()
        #vsqrname
        if self.vsqrname==None:
            name='prj'
            sqr_str = "uvm_test_top.env.%s"%initial_vseqr
        else:
            sqr_str = "uvm_test_top.env.%s"%self.vsqrname[0]
        #excelname
        if self.excelname==None:
            excel_name = initial_excel_name
        else:
            excel_name = "%s"%self.excelname[0]
        #sheetname
        if self.sheetname==None:
            sheet_name = initial_sheet_name
        else:
            sheet_name = self.sheetname[0]
        #wavepath
        if self.wavepath==None:
            wave_path = initial_wave_path
        else:
            wave_path = "%s"%self.wavepath[0]

        #Display the intialization
        if self.args.log:
            print("=======================================================")
            print("initial_vseqr        = %s"%initial_vseqr)
            print("initial_excel_name   = %s"%initial_excel_name)
            print("initial_sheet_name   = %s"%initial_sheet_name)
            print("initial_wave_path    = %s"%initial_wave_path)
            print("=======================================================")

        self.excel_to_json_file(excel_name,sheet_name,wave_path,sqr_str,PrintEnable=True)
    
    def GetArgs(self):
        parser = argparse.ArgumentParser(description='EzChip Testbench Flow Args Parser')
        parser.add_argument('-vsqr'     , nargs="+"      , dest="vsqrname"      , default=None  , help="Please give the vsqr instance name")
        parser.add_argument('-excel'    , nargs='+'      , dest="excelname"     , default=None  , help="Please give the excel file of the case")
        parser.add_argument('-sheet'    , nargs='+'      , dest="sheetname"     , default=None  , help="Please give the name of the case sheet in the excel file")
        parser.add_argument('-wave'     , nargs='+'      , dest="wavepath"      , default=None  , help="Give the path to the tcl file of wave")
        parser.add_argument('-l'    , action='store_true', dest="log"           , default=False , help="The initialization information is displayed")
        self.args = parser.parse_args()

        #vsqrname
        if not self.args.vsqrname==None:
            self.vsqrname=self.args.vsqrname
        else:
            self.vsqrname=None
        #excelname
        if not self.args.excelname==None:
            self.excelname=self.args.excelname
        else:
            self.excelname=None
        #sheetname
        if not self.args.sheetname==None:
            self.sheetname=self.args.sheetname
        else:
            self.sheetname=None
        #wavepath
        if not self.args.wavepath==None:
            self.wavepath=self.args.wavepath
        else:
            self.wavepath=None
        
    def excel_to_json_file(self,excel_name,sheet_name,wave_path,sqr_str,PrintEnable):
        print("Conversion start")
        self.read_Excel(excel_name,sheet_name,wave_path,sqr_str)
        self.excel_to_json_group()
        print("Conversion succeeded")

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")

    def read_Excel(self,excel_name,sheet_name,wave_path,sqr_str):
        wb = openpyxl.load_workbook(excel_name)     # 打开文件
        sheet = wb[sheet_name]                      # 通过sheet名称锁定表格
        for row in sheet.rows:                      # 循环所有的行
            list_release = []
            for cell in row:                        # 循环行中所有的单元格
                list_release.append(cell.value)

            if list_release[0] == None:
                return
            elif "_test" in list_release[0]:
                self.process_to_json(list_release,wave_path,list_release[2],sqr_str)
            else:
                pass
        #print("[read_Excel] finish")

    def process_to_json(self,json_list,wave_path,json_name,sqr_str):
        #print("[process_to_json] start")
        varb = "'b"
        varh = "'h"
        json_all = []
        json_pt = []
        str_list = []

        list_json = json_list
        release_dirt = {'uvm_testname':'test',"sim_args":'test',"tcl": wave_path,"timescale":"1ns/1ps"}
        release_dirt["uvm_testname"] = list_json[4]
        list_json[3] = list_json[3].replace(';', '')
        list_json[3] = re.split('\n |=', list_json[3])
        a = 1
        while a<len(list_json[3]):
            if list_json[3][a].isdigit():
                string1 = '%s%s,%s,%s%s' % ('+uvm_set_config_int=\"', sqr_str, list_json[3][a - 1], list_json[3][a], '\"')
                str_list.append(string1)
            else:
                if varb in list_json[3][a]:
                    list_json[3][a] = list_json[3][a].replace("'b", '')
                    list_json[3][a] = int(list_json[3][a], 2)
                    string1 = '%s%s%s,%s%s' % ('+uvm_set_config_int=\"', sqr_str, list_json[3][a - 1], list_json[3][a], '\"')
                    str_list.append(string1)
                elif varh in list_json[3][a]:
                    list_json[3][a] = list_json[3][a].replace("'h", '')
                    list_json[3][a] = int(list_json[3][a], 16)
                    string1 = '%s%s.%s,%s%s' % ('+uvm_set_config_int=\"', sqr_str, list_json[3][a - 1], list_json[3][a], '\"')
                    str_list.append(string1)
                else:
                    string1 = '%s%s.%s,%s%s' % ('+uvm_set_config_string=\"', sqr_str, list_json[3][a - 1], list_json[3][a], '\"')
                    str_list.append(string1)
            a = a+2
        string3 = ''.join(str_list)
        str_list.clear()
        release_dirt["sim_args"] = string3
        json_all = {list_json[0]: release_dirt}
        json_pt.append(json_all)
        json_str1 = json.dumps(json_pt)
        json_str2 = json_str1.replace('[', '')
        json_str3 = json_str2.replace(']', '')
        json_str4 = json_str3.replace('}, {', ',')
        json_str5 = json_str4.replace('{', '{\n')
        json_str6 = json_str5.replace('",', '",\n')
        json_str7 = json_str6.replace('},', '},\n')
        json_str8 = json_str7.replace('1ps"', '1ps"\n')
        json_str9 = json_str8.replace('"uvm_testname"', ' "uvm_testname"')
        json_str10 = json_str9.replace('"sim_args"', ' "sim_args"')
        json_str11 = json_str10.replace('"tcl"', ' "tcl"')
        json_str12 = json_str11.replace('"timescale"', ' "timescale"')
        json_str = json_str12.replace('*', '[*]')

        self.json_name.append(json_name)
        self.json_strstr.append(json_str)

    def excel_to_json_group(self):
        # If the file exists, delete it first
        for i in range(len(self.json_name)):
            if os.path.isfile("%s.json"%self.json_name[i]):
                os.remove("%s.json"%self.json_name[i])

        # Add "{" to first line of file
        for i in range(len(self.json_name)):
            jsonfile = open("%s.json"%self.json_name[i], 'a') 
            with open('%s.json'%self.json_name[i],'r',encoding='utf-8') as f:
                lines=f.readline()
                if lines=='':
                    jsonfile.write("{")
                    jsonfile.close()
                else:
                    jsonfile.close()
        # Add json content
        for i in range(len(self.json_name)):            
            jsonfile = open("%s.json"%self.json_name[i], 'a') 
            jsonfile.write("%s,"%self.json_strstr[i][1:-1])
            jsonfile.close()

        # Add '} 'at the end of the file
        for i in range(len(self.json_name)):
            jsonfile = open("%s.json"%self.json_name[i], 'a') 
            with open('%s.json'%self.json_name[i],'r',encoding='utf-8') as f:
                lines=f.readlines()
                lastlines=lines[-1]
                if lastlines=='},':
                    jsonfile.write("}")
                    jsonfile.close()
                else:
                    jsonfile.close()

        # Read before you write
        for i in range(len(self.json_name)):
            newlines=[]
            with open('%s.json'%self.json_name[i],'r',encoding='utf-8') as f:
                lines=f.readlines()
                for j in range(len(lines)):
                    if lines[j] == '},}':
                        newlines.append("}}")
                    else:
                        newlines.append(lines[j])

            with open('%s.json'%self.json_name[i],'w',encoding='utf-8') as f:
                for j in range(len(newlines)):
                    f.write(newlines[j])
     
if __name__ == '__main__':
    gen=excel_to_json()