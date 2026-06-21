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

class gen_testcase_TestTop:

    def __init__(self):
        print("[gen_testcase_TestTop]:initial")
        #EnvironmentGenCfg='../VerifyEnvironmentGenCfg.xlsx'
        EnvironmentGenCfg=Parameters.EnvironmentGenCfg
        readexcel_WorkingDirectoryGen.readexcel_WorkingDirectoryGen_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_VIP.readexcel_VIP_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_ClockRst.readexcel_ClockRst_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_DutSignal.readexcel_DutSignal_info(self,EnvironmentGenCfg,PrintEnable=False)
        self.gen_testcase_TestTop_info(self.tb_name,PrintEnable=True)

    def gen_testcase_TestTop_info(self,name,PrintEnable):
        filename = open("%s_TestTop.svh"%name, "w+")
        filename.write("`ifndef _%s_TEST_TOP_SV_\n"%name.upper())
        filename.write("`define _%s_TEST_TOP_SV_\n"%name.upper())
        filename.write("\n")
        filename.write("package %s_TestTop;\n"%name)
        filename.write("\n")
        filename.write("\timport uvm_pkg::*;\n")
        filename.write("\t`include \"uvm_macros.svh\"\n")
        filename.write("\n")
        filename.write("\t//import the SVT UVM PKG\n")
        svt_pkg=False
        for VipName in self.VIP_DB.keys():
            if self.VIP_DB[VipName]['Enable']:
                svt_pkg=True
        if svt_pkg==True:
            filename.write("\timport svt_uvm_pkg::*;\n")
        else:
            filename.write("\t//import svt_uvm_pkg::*;\n")
            
        # #vip top
        # #if self.vip_apb_enable:
        # if self.VIP_DB['APB']['Enable']:
        #     filename.write("\timport svt_apb_uvm_pkg::*;\n")
        #     filename.write("\n")
        # #if self.vip_ahb_enable:
        # if self.VIP_DB['AHB']['Enable']:
        #     filename.write("\timport svt_ahb_uvm_pkg::*;\n")
        #     filename.write("\n")
        # #if self.vip_axi_enable:
        # if self.VIP_DB['AXI']['Enable']:
        #     filename.write("\timport svt_axi_uvm_pkg::*;\n")
        #     filename.write("\n")
        for VipName in self.VIP_DB.keys():
            if self.VIP_DB[VipName]['Enable']:
                filename.write("\timport svt_%s_uvm_pkg::*;\n"%VipName.lower())
        filename.write("\n")
        for VipName in self.VIP_DB.keys():
            if self.VIP_DB[VipName]['Enable']:
                filename.write("\timport %s_UvcTop::*;\n"%VipName.lower())
        filename.write("\n")
        #uvc top
        for i in range(len(self.DUT_GroupName)):
            if self.DUT_VIP[i]==True:
                filename.write("\t`ifndef NO_%s_CUSTOM\n"%self.DUT_GroupName[i])
            filename.write("\timport %s_UvcTop::*;\n"%self.DUT_GroupName[i])
            if self.DUT_VIP[i]==True:
                filename.write("\t`endif\n")
        filename.write("\n")
        #env top
        filename.write("\timport %s_EnvTop::*;\n"%name)
        filename.write("\n")
        filename.write("\t`include \"%s_sequence_lib.sv\"\n"%name)
        filename.write("\t`include \"%s_base_test.sv\"\n"%name)
        filename.write("\n")
        filename.write("\t`include \"%s_demo_test.sv\"\n"%name)
        filename.write("\n")
        filename.write("endpackage\n")
        filename.write("`endif\n")
        filename.close()

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")

if __name__ == '__main__':
    gen=gen_testcase_TestTop()