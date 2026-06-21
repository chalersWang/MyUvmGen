#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os

class gen_tcl_file:

    def __init__(self):
        print("[gen_tcl_file]:initial")
        self.gen_tcl_file_info(tb_name=None,PrintEnable=True)

    def gen_tcl_file_info(self,tb_name,PrintEnable):
        if tb_name==None:
            filename = open("wave.tcl", "w+")
        else:
            filename = open("%s_wave.tcl"%tb_name, "w+")
        filename.write("proc fsdb_dump {} {\n")
        filename.write("\tfsdbDumpfile \"sim.fsdb\"\n")
        filename.write("\tfsdbDumpvars 0 tb_top\n")
        filename.write("\tfsdbDumpMDA 0 tb_top\n")
        filename.write("\tfsdbDumpon\n")
        filename.write("}\n")
        filename.write("\n")
        filename.write("if {$env(MY_FSDB_DUMP) == \"on\"} {\n")
        filename.write("\tfsdb_dump\n")
        filename.write("}\n")
        filename.write("run\n")
        filename.close()

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")

if __name__ == '__main__':
    gen=gen_tcl_file()