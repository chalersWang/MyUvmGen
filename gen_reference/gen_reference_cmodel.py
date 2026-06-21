#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from common_lib.parameters import Parameters

class gen_reference_cmodel:

    def __init__(self):
        print("[gen_reference_cmodel]:initial")
        name=Parameters.tb_name
        self.gen_reference_cmodel_info(name,PrintEnable=True)

    def gen_reference_cmodel_info(self,name,PrintEnable):
        filename = open("%s_cmodel.sv"%name, "w+")
        filename.write("`ifndef %s_CMODEL_SV\n"%name.upper())
        filename.write("`define %s_CMODEL_SV\n"%name.upper())
        filename.write("\n")
        filename.write("//  import \"DPI-C\" function void cmodel(input int aa[10],input bit[7:0]bb[20],output bit[7:0]cc[30]);\n")
        filename.write("//  import \"DPI-C\" function void cmethod();\n")
        filename.write("\n")
        filename.write("//  class %s_cmodel;\n"%name)
        filename.write("//  \tint       a[10];\n")
        filename.write("//  \tbit[7:0]  b[20];\n")
        filename.write("//  \tbit[7:0]  c[30];\n")
        filename.write("\n")
        filename.write("//  \tfunction void cfun(input int a[10],input bit[7:0]b[20],output bit[7:0]c[30]);\n")
        filename.write("//  \t\tcmodel(a,b,c);\n")
        filename.write("//  \t\tcmethod();\n")
        filename.write("//  \tendfunction\n")
        filename.write("\n")
        filename.write("//  endclass\n")
        filename.write("\n")
        filename.write("`endif\n")
        filename.write("\n")

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")

if __name__ == '__main__':
    gen=gen_reference_cmodel()