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

class gen_sva_file:

    def __init__(self):
        print("[gen_sva_file]:initial")
        #EnvironmentGenCfg='../VerifyEnvironmentGenCfg.xlsx'
        EnvironmentGenCfg=Parameters.EnvironmentGenCfg
        readexcel_WorkingDirectoryGen.readexcel_WorkingDirectoryGen_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_VIP.readexcel_VIP_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_ClockRst.readexcel_ClockRst_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_DutSignal.readexcel_DutSignal_info(self,EnvironmentGenCfg,PrintEnable=False)
        self.gen_sva_file_info(PrintEnable=True)

    def gen_sva_file_info(self,PrintEnable):
        #VifMacroDefine.v
        #filename = open("VifMacroDefine.v", "w+")
        filename = open(Parameters.SvaVifDefine, "w+")
        filename.write("`define %s_TOP_VIF     tb_top.DUT\n"%self.tb_name.upper())
        filename.write("\n")
        for i in range(len(self.DUT_GroupName)):
            if self.DUT_VIP[i]==False:
                filename.write("`define %s_%s_VIF     `%s_TOP_VIF\n"%(Parameters.macro_name,self.DUT_GroupName[i].upper(),self.tb_name.upper()))
        filename.close()
        #xx_vif.v
        filename = open("%s_vif.sv"%self.tb_name, "w+")
        filename.write("`ifndef _%s_VIF_SV_\n"%self.tb_name.upper())
        filename.write("`define _%s_VIF_SV_\n"%self.tb_name.upper())
        filename.write("\n")
        filename.write("interface %s_vif(input clk,input rstn);\n"%self.tb_name)
        filename.write("\n")
        filename.write("\tstring   TestCaseName;\n")
        filename.write("\n")
        for i in range(len(self.DUT_GroupName)):
            if self.DUT_VIP[i]==False:
                filename.write("\t%s_vif %svif(clk,rstn);\n"%(self.DUT_GroupName[i],self.DUT_GroupName[i]))
            else:
                filename.write("\t`ifndef NO_%s_CUSTOM\n"%self.DUT_GroupName[i])
                filename.write("\t%s_vif %svif(clk,rstn);\n"%(self.DUT_GroupName[i],self.DUT_GroupName[i]))
                filename.write("\t`endif\n")
        filename.write("\n")
        filename.write("//\t`ifdef SVA_VIF_TOP\n")
        filename.write("//\t\t`include\"./sva_code/sva_vif_top.sv\"\n")
        filename.write("//\t`endif\n")
        filename.write("//\n")
        # filename.write("//\tfunction GetTestCaseName(string casename);\n")
        # filename.write("//\t\treturn(TestCaseName==casename);\n")
        # filename.write("//\tendfunction\n")
        filename.write("\n")
        filename.write("endinterface\n")
        filename.write("\n")
        filename.write("`endif\n")
        filename.write("\n")
        filename.close()
        #[sva_code]
        if not os.path.isdir('code'):
            os.mkdir('code')
        os.chdir('code')
        filename = open("sva_tb_top.sv", "w+")
        filename.close()
        filename = open("sva_vif_top.sv", "w+")
        filename.close()
        for i in range(len(self.DUT_GroupName)):
            # if self.DUT_VIP[i]==False:
                filename = open("sva_vif_%s.sv"%self.DUT_GroupName[i], "w+")
                filename.close()
                
        #filename = open("AssertionHierarchy.lst", "w+")
        filename = open(Parameters.SvaHierarchyFile, "w+")
        filename.write("//-tree tb_top.DUT.xx\n")
        filename.write("//+tree tb_top.DUT.xx1\n")
        filename.close()

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")

if __name__ == '__main__':
    gen=gen_sva_file()