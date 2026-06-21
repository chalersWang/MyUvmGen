#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os

class gen_uvc_UvcTop:

    def __init__(self):
        print("[gen_uvc_UvcTop]:initial")
        self.gen_uvc_UvcTop_info(name='xx',PrintEnable=True)

    def gen_uvc_UvcTop_info(self,name,PrintEnable):
        filename = open("%s_UvcTop.svh"%name, "w+")
        filename.write("`ifndef _%s_UVC_TOP_SVH_\n"%name.upper())
        filename.write("`define _%s_UVC_TOP_SVH_\n"%name.upper())
        filename.write("\n")
        filename.write("`include \"uvm_macros.svh\"\n")
        filename.write("\n")
        filename.write("package %s_UvcTop;\n"%name)
        filename.write("\n")
        filename.write("\timport uvm_pkg::*;\n")
        filename.write("\n")
        filename.write("\ttypedef   class %s_config;\n"%name)
        filename.write("\ttypedef   class %s_trans;\n"%name)
        filename.write("\ttypedef   class %s_driver;\n"%name)
        filename.write("\ttypedef   class %s_monitor;\n"%name)
        filename.write("\ttypedef   class %s_sequencer;\n"%name)
        filename.write("\ttypedef   class %s_agent;\n"%name)
        filename.write("\ttypedef   class %s_sequence_lib;\n"%name)
        filename.write("\n")
        filename.write("\t`include \"%s_config.sv\"\n"%name)
        filename.write("\t`include \"%s_trans.sv\"\n"%name)
        filename.write("\t`include \"%s_driver.sv\"\n"%name)
        filename.write("\t`include \"%s_monitor.sv\"\n"%name)
        filename.write("\t`include \"%s_sequencer.sv\"\n"%name)
        filename.write("\t`include \"%s_agent.sv\"\n"%name)
        filename.write("\t`include \"%s_sequence_lib.sv\"\n"%name)
        filename.write("\n")
        filename.write("endpackage\n")
        filename.write("\n")
        filename.write("`endif\n")
        filename.close()

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")


if __name__ == '__main__':
    gen=gen_uvc_UvcTop()