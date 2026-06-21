#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#sys.path.append(r".\..\readexcel")
from common_lib.parameters import Parameters

class gen_DirectoryStructure:

    def __init__(self):
        print("[gen_DirectoryStructure]:initial")
        local_dir   ='./'
        #tb_name     ='prj'
        #PrintEnable =True
        tb_name     =Parameters.tb_name
        PrintEnable =Parameters.PrintEnable
        self.gen_DirectoryStructure_info(local_dir,tb_name,PrintEnable)

    def gen_DirectoryStructure_info(self,local_dir,tb_name,PrintEnable):
        os.chdir(local_dir)
        # create dir of prj
        if not os.path.isdir(tb_name):
            os.mkdir(tb_name)
        os.chdir(tb_name)
        self.local_dir = os.getcwd()

        #create dir of "cfg"
        if not os.path.isdir('cfg'):
            os.mkdir('cfg')
        os.chdir(self.local_dir)
        #create dir of "filelist"
        if not os.path.isdir('filelist'):
            os.mkdir('filelist')
        os.chdir(self.local_dir)
        #create dir of "tb"
        if not os.path.isdir('tb'):
            os.mkdir('tb')
        os.chdir(self.local_dir)
        #create dir of "env"
        if not os.path.isdir('env'):
            os.mkdir('env')
        os.chdir(self.local_dir)
        #create dir of "reference"
        if not os.path.isdir('reference'):
            os.mkdir('reference')
        os.chdir(self.local_dir)
        #create dir of "regmodel"
        if not os.path.isdir('regmodel'):
            os.mkdir('regmodel')
        os.chdir(self.local_dir)
        #create dir of "uvc"
        if not os.path.isdir('uvc'):
            os.mkdir('uvc')
        os.chdir(self.local_dir)
        #create dir of "sva"
        if not os.path.isdir('sva'):
            os.mkdir('sva')
        os.chdir(self.local_dir)
        #create dir of "coverage"
        if not os.path.isdir('coverage'):
            os.mkdir('coverage')
        os.chdir('coverage')
        if not os.path.isdir('code'):
            os.mkdir('code')
        # if not os.path.isdir('coverage_result_case'):
        #     os.mkdir('coverage_result_case')
        if not os.path.isdir('result'):
            os.mkdir('result')
        os.chdir(self.local_dir)
        #create dir of "testcase"
        if not os.path.isdir('testcase'):
            os.mkdir('testcase')
        os.chdir(self.local_dir)
        #create dir of "testplan"
        if not os.path.isdir('testplan'):
            os.mkdir('testplan')
        os.chdir(self.local_dir)
        #create dir of "run"
        if not os.path.isdir('run'):
            os.mkdir('run')
        os.chdir(self.local_dir)
        #create dir of "tcl"
        if not os.path.isdir('tcl'):
            os.mkdir('tcl')
        os.chdir(self.local_dir)
        #create dir of "json"
        if not os.path.isdir('json'):
            os.mkdir('json')
        os.chdir(self.local_dir)
        #create dir of "script"
        if not os.path.isdir('script'):
            os.mkdir('script')
        os.chdir(self.local_dir)

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")

if __name__ == '__main__':
    gen=gen_DirectoryStructure()