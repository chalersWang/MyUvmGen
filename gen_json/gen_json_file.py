#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

class gen_json_file:

    def __init__(self):
        print("[gen_json_file]:initial")
        self.gen_json_file_info(jsonname='wxx',PrintEnable=True)

    def gen_json_file_info(self,jsonname,PrintEnable):
        # Read before you write
        newlines=[]
        srcpath=os.path.split(os.path.realpath(__file__))[0]
        with open('%s/excel_to_json.py'%srcpath,'r',encoding='utf-8') as f:
            lines=f.readlines()
            for j in range(len(lines)):
                if lines[j] == '},}':
                    newlines.append("}}")
                else:
                    newlines.append(lines[j])
        dstpath=os.getcwd()
        with open('%s/%s.py'%(dstpath,jsonname),'w',encoding='utf-8') as f:
            for j in range(len(newlines)):
                f.write(newlines[j])

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")
            print(srcpath)
            print(dstpath)

if __name__ == '__main__':
    gen=gen_json_file()