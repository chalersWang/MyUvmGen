#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os
import re
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

class read_kfile:

    def __init__(self):
        print("[read_kfile]:initial")
        self.kfileToffile_define=[]
        filepath='./demo.cfg'
        self.read_kfile_info(filepath,PrintEnable=True)
    
    def read_kfile_info(self,filepath,PrintEnable):

        # with open(filepath,'r') as f:
        #     lines=f.readlines()
        #     for i in range(len(lines)):
        #         print("lines=%s"%lines[i].strip("\n")[:2])


        if os.path.isfile(filepath):
            lines=open(filepath,"r").read()
            result=""
            self.kfileToffile_define = re.findall(r"[+]define[+](.*?)\n", lines)
            result = result +'\n'.join(self.kfileToffile_define)
            print(self.kfileToffile_define)
        else:
            print("The path of file is not exist!!! Please ensure the path of the filename.k")

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")

if __name__ == '__main__':
    gen=read_kfile()