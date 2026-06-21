#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

class gen_run_file:

    def __init__(self):
        print("[gen_run_file]:initial")
        self.gen_run_file_info(runname='runrun',PrintEnable=True)
        self.gen_xrun_file_info(xrunname='xrunxrun',PrintEnable=True)

    def gen_run_file_info(self,runname,PrintEnable):
        # Read before you write
        newlines=[]
        srcpath=os.path.split(os.path.realpath(__file__))[0]
        with open('%s/run.py'%srcpath,'r',encoding='utf-8') as f:
            lines=f.readlines()
            for j in range(len(lines)):
                if lines[j] == '},}':
                    newlines.append("}}")
                else:
                    newlines.append(lines[j])
        dstpath=os.getcwd()
        with open('%s/%s'%(dstpath,runname),'w',encoding='utf-8') as f:
            for j in range(len(newlines)):
                f.write(newlines[j])

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")
            # print(srcpath)
            # print(dstpath)

    def gen_xrun_file_info(self,xrunname,PrintEnable):
        # Read before you write
        newlines=[]
        srcpath=os.path.split(os.path.realpath(__file__))[0]
        # with open('%s/xrun.py'%srcpath,'r',encoding='utf-8') as f:
        with open('%s/mrun.py'%srcpath,'r',encoding='utf-8') as f:
            lines=f.readlines()
            for j in range(len(lines)):
                if lines[j] == '},}':
                    newlines.append("}}")
                else:
                    newlines.append(lines[j])
        dstpath=os.getcwd()
        with open('%s/%s'%(dstpath,xrunname),'w',encoding='utf-8') as f:
            for j in range(len(newlines)):
                f.write(newlines[j])

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")
            # print(srcpath)
            # print(dstpath)
    
    def gen_makefile_file_info(self,makefilename,PrintEnable):
        # Read before you write
        newlines=[]
        srcpath=os.path.split(os.path.realpath(__file__))[0]
        with open('%s/Makefile'%srcpath,'r',encoding='utf-8') as f:
            lines=f.readlines()
            for j in range(len(lines)):
                if lines[j] == '},}':
                    newlines.append("}}")
                else:
                    newlines.append(lines[j])
        dstpath=os.getcwd()
        with open('%s/%s'%(dstpath,makefilename),'w',encoding='utf-8') as f:
            for j in range(len(newlines)):
                f.write(newlines[j])

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")
            # print(srcpath)
            # print(dstpath)

if __name__ == '__main__':
    gen=gen_run_file()