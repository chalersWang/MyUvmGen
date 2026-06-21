#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os
import sys
sys.path.append(r".\..") 

script_path=os.path.split(os.path.realpath(__file__))[0]
print("[Script] : %s [Path]: %s"%(os.path.basename(__file__),script_path))

from common_lib.parameters import Parameters
from common_lib.common_lib import PrintLog
from common_lib.common_lib import GetFileName
from common_lib.common_lib import CreateDir
from common_lib.common_lib import CopyFile
from common_lib.common_lib import CreateFileLink

class gen_testplan_file:

    def __init__(self):
        print("[gen_testplan_file]:initial")
        JsonPath    =script_path+'/../gen_json'
        FilelistPath=script_path+'/../gen_filelist'
        self.gen_testplan_file_info(JsonPath,FilelistPath,PrintEnable=True)

    def gen_testplan_file_info(self,JsonPath,FilelistPath,PrintEnable):
        PrintLog(self,"[gen_testplan_file]:gen_testplan_file_info",PrintEnable)
        #Suffix  ='.json'
        Suffix  =Parameters.JsonSuffix
        Slash   =Parameters.slash

        if os.path.isdir(JsonPath):
            FileList=GetFileName(self,JsonPath,Suffix)
            for i in range(len(FileList)):
                filename=FileList[i][:-5]       #5:len(Suffix)
                #print(FileList[i][:-5])
                CreateDir(self,filename)
                CopyFile(self,JsonPath+Slash+FileList[i],filename+Slash+"test.json")
                # CreateFileLink(self,FilelistPath+Slash+'rtl.f'      ,filename+Slash+'rtl.f')
                # CreateFileLink(self,FilelistPath+Slash+'vip.f'      ,filename+Slash+'vip.f')
                # CreateFileLink(self,FilelistPath+Slash+'tb.f'       ,filename+Slash+'tb.f')
                # CreateFileLink(self,FilelistPath+Slash+'cmodel.f'   ,filename+Slash+'cmodel.f')
                # CreateFileLink(self,FilelistPath+Slash+Parameters.Filelist_define   ,filename+Slash+Parameters.Filelist_define)
                CreateFileLink(self,FilelistPath+Slash+Parameters.Filelist_rtl      ,filename+Slash+Parameters.Filelist_rtl)
                CreateFileLink(self,FilelistPath+Slash+Parameters.Filelist_vip      ,filename+Slash+Parameters.Filelist_vip)
                CreateFileLink(self,FilelistPath+Slash+Parameters.Filelist_tb       ,filename+Slash+Parameters.Filelist_tb)
                CreateFileLink(self,FilelistPath+Slash+Parameters.Filelist_cmodel   ,filename+Slash+Parameters.Filelist_cmodel)
        else:
            raise Exception("The path of json is not exist!!!")

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")

if __name__ == '__main__':
    gen=gen_testplan_file()