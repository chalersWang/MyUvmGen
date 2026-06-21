#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from readexcel.readexcel_WorkingDirectoryGen import readexcel_WorkingDirectoryGen
from readexcel.readexcel_VIP import readexcel_VIP
from readexcel.readexcel_DutSignal import readexcel_DutSignal
from readexcel.readexcel_ClockRst import readexcel_ClockRst
from common_lib.parameters import Parameters

class gen_env_function_coverage:

    def __init__(self):
        print("[gen_env_EnvTop]:initial")
        #EnvironmentGenCfg='../VerifyEnvironmentGenCfg.xlsx'
        EnvironmentGenCfg=Parameters.EnvironmentGenCfg
        readexcel_WorkingDirectoryGen.readexcel_WorkingDirectoryGen_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_VIP.readexcel_VIP_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_ClockRst.readexcel_ClockRst_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_DutSignal.readexcel_DutSignal_info(self,EnvironmentGenCfg,PrintEnable=False)
        self.gen_env_function_coverage_info(PrintEnable=True)

    def gen_env_function_coverage_info(self,PrintEnable):
         #*_function_coverage.sv    
        filename = open("%s_function_coverage.sv"%self.tb_name, "w+")
        filename.write("`ifndef _%s_FUNCTION_COVERAGE_SV_\n" %self.tb_name.upper())
        filename.write("`define _%s_FUNCTION_COVERAGE_SV_\n" %self.tb_name.upper())
        filename.write("\n")
        filename.write("//Add a specific function coverage code\n")
        filename.write("\n")
        filename.write("\t//Examples are as follows\n")
        for i in range(len(self.DUT_GroupName)):
            filename.write("\t`ifdef COVERAGE_%s\n"%self.DUT_GroupName[i].upper())
            if self.DUT_VIP[i]==False:
                filename.write("\t\t`include\"%s_function_coverage.sv\"\n"%self.DUT_GroupName[i])
            else:
                filename.write("\t`ifndef NO_%s_CUSTOM\n"%self.DUT_GroupName[i])
                filename.write("\t\t`include\"%s_function_coverage.sv\"\n"%self.DUT_GroupName[i])
                filename.write("\t`endif\n")
            filename.write("\t`endif\n")
        filename.write("\n")
        filename.write("`endif\n")
        filename.write("\n")
        filename.close()

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")

if __name__ == '__main__':
    gen=gen_env_function_coverage()