#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os

from common_lib.parameters import Parameters
from common_lib.common_lib import gen_uvm_new
from common_lib.common_lib import gen_uvm_phase

class gen_uvc_sequencer:

    def __init__(self):
        print("[gen_uvc_sequencer]:initial")
        self.gen_uvc_sequencer_info(name='xx',PrintEnable=True)

    def gen_uvc_sequencer_info(self,name,PrintEnable):
        filename = open("%s_sequencer.sv"%name, "w+")
        filename.write("`ifndef _%s_SEQUENCER_SV_\n"%name.upper())
        filename.write("`define _%s_SEQUENCER_SV_\n"%name.upper())
        filename.write("\n")
        filename.write("class %s_sequencer extends uvm_sequencer#(%s_trans);\n"%(name,name))
        filename.write("\n")
        filename.write("\t`uvm_component_utils(%s_sequencer)\n"%name)
        filename.write("\n")
        # filename.write("\tfunction new(string name,uvm_component parent);\n")
        # filename.write("\t\tsuper.new(name,parent);\n")
        # filename.write("\tendfunction\n")
        # filename.write("\n")
        gen_uvm_new(self,filename,'%s_sequencer'%name,'uvm_component',None,Parameters.PrintEnable)
        
        filename.write("endclass\n")
        filename.write("\n")
        filename.write("`endif\n")
        filename.close()

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")


if __name__ == '__main__':
    gen=gen_uvc_sequencer()