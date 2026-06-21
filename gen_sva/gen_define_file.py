
#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from readexcel.readexcel_WorkingDirectoryGen import readexcel_WorkingDirectoryGen
from readexcel.readexcel_DutSignal import readexcel_DutSignal
from common_lib.parameters import Parameters

class gen_define_file:

    def __init__(self):
        print("[gen_define_file]:initial")
        # #EnvironmentGenCfg='../VerifyEnvironmentGenCfg.xlsx'
        # EnvironmentGenCfg=Parameters.EnvironmentGenCfg
        # readexcel_WorkingDirectoryGen.readexcel_WorkingDirectoryGen_info(self,EnvironmentGenCfg,PrintEnable=False)
        # readexcel_DutSignal.readexcel_DutSignal_info(self,EnvironmentGenCfg,PrintEnable=False)
        self.gen_define_file_info(PrintEnable=True)

    def gen_define_file_info(self,PrintEnable):
        filename = open("define_lib.v", "w+")
        filename.write("//============= %s Common Project Lib ===============================\n"%Parameters.COMPANY)
        filename.write("//<1> gen random data\n")
        filename.write("    `define %s_GEN_RAND_32BIT\\\n"%Parameters.COMPANY)
        filename.write("        $random()\n")
        filename.write("\n")
        filename.write("    `define %s_GEN_RAND_64BIT\\\n"%Parameters.COMPANY)
        filename.write("        {$random,$random}\n")
        filename.write("\n")
        filename.write("    `define %s_GEN_RAND_128BIT\\\n"%Parameters.COMPANY)
        filename.write("        {$random,$random,$random,$random}\n")
        filename.write("\n")
        filename.write("//<2> DELAY\n")
        filename.write("    `define %s_DELAY(cnt)\\\n"%Parameters.COMPANY)
        filename.write("        #(``cnt``);\n")
        filename.write("\n")
        filename.write("//<3> UVM_HDL_FORCE\n")
        filename.write("    `define %s_DELCARE_SIGNAL_STRING(Signal,SignalPath)\\\n"%Parameters.COMPANY)
        filename.write("        string ``Signal``=\"``SignalPath\";\n")
        filename.write("\n")
        filename.write("//<4> wait for rst release\n")
        filename.write("    `define %s_WAIT_RST_RELEASE()\\\n")
        filename.write("        @(posedge rstn);\n")
        filename.write("\n")
        filename.write("//<5> coonfigdb\n")
        filename.write("    `define %s_CONFIG_DB_SET(vifname,InfInst)\\\n"%Parameters.COMPANY)
        filename.write("        uvm_config_db#(virtual ``vifname``)::set(null,\"*\",\"``vifname``\",``InfInst``);\n")
        filename.write("\n")
        filename.write("    `define %s_CONFIG_DB_GET(vifname,InfInst)\\\n"%Parameters.COMPANY)
        filename.write("        uvm_config_db#(virtual ``vifname``)::get(null,get_full_name(),\"``vifname``\",``InfInst``);\n")
        filename.write("\n")
        filename.write("//============= %s Common Macro Lib =================================\n"%Parameters.COMPANY)
        filename.write("//<1>colour\n")
        filename.write("    `define %s_RESET    \"\\033[0m\"\n"%Parameters.COMPANY)
        filename.write("    `define %s_RED      \"\\033[31m\"\n"%Parameters.COMPANY)
        filename.write("    `define %s_GREEN    \"\\033[32m\"\n"%Parameters.COMPANY)
        filename.write("    `define %s_YELLOW   \"\\033[33m\"\n"%Parameters.COMPANY)
        filename.write("    `define %s_BLUE     \"\\033[34m\"\n"%Parameters.COMPANY)
        filename.write("\n")
        filename.write("//<2>message\n")
        filename.write("    `define %s_SetColour(colour,message)\\\n"%Parameters.COMPANY)
        filename.write("        $sformatf(\"%s%s\\033[0m\",``colour``,``message``)\n")
        filename.write("\n")
        filename.write("    `define %s_INFO(message)\\\n"%Parameters.COMPANY)
        filename.write("        `uvm_info(`%s_SetColour(`%s_YELLOW,get_full_name()),`%s_SetColour(`%s_GREEN,``message``),UVM_LOW)\n"%(Parameters.COMPANY,Parameters.COMPANY,Parameters.COMPANY,Parameters.COMPANY))
        filename.write("\n")
        filename.write("    `define %s_WARNING(message)\\\n"%Parameters.COMPANY)
        filename.write("        `uvm_warning(get_full_name(),$sformatf(\"\\033[33m%s\\033[0m\",``message``))\n")
        filename.write("\n")
        filename.write("    `define %s_ERROR(message)\\\n"%Parameters.COMPANY)
        filename.write("        `uvm_error(get_full_name(),$sformatf(\"\\033[31m%s\\033[0m\",``message``))\n")
        filename.write("\n")
        filename.write("    `define %s_FATAL(message)\\\n"%Parameters.COMPANY)
        filename.write("        `uvm_fatal(get_full_name(),$sformatf(\"\\033[31m%s\\033[0m\",``message``))\n")
        filename.write("\n")
        filename.write("//<3>display\n")
        filename.write("    `define %s_DISPLAY(Signal)\\\n"%Parameters.COMPANY)
        filename.write("        $display(\"``Signal``=%0h\",``Signal``);\n")
        filename.write("\n")
        filename.write("    `define %s_DISPLAY_ARRAY(Signal)\\\n"%Parameters.COMPANY)
        filename.write("        foreach(``Signal``[i])begin\\\n")
        filename.write("            $display(\"``Signal``[i]=%0h\",``Signal``[i]);\\\n")
        filename.write("        end\n")
        filename.write("\n")
        filename.close()

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")

if __name__ == '__main__':
    gen=gen_define_file()