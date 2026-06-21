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

class gen_env_EnvTop:

    def __init__(self):
        print("[gen_env_EnvTop]:initial")
        #EnvironmentGenCfg='../VerifyEnvironmentGenCfg.xlsx'
        EnvironmentGenCfg=Parameters.EnvironmentGenCfg
        readexcel_WorkingDirectoryGen.readexcel_WorkingDirectoryGen_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_VIP.readexcel_VIP_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_ClockRst.readexcel_ClockRst_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_DutSignal.readexcel_DutSignal_info(self,EnvironmentGenCfg,PrintEnable=False)
        self.gen_env_EnvTop_info(PrintEnable=True)

    def gen_env_EnvTop_info(self,PrintEnable):
        filename = open("%s_EnvTop.svh"%self.tb_name, "w+")
        filename.write("`ifndef _%s_EnvTop_SV_\n" %self.tb_name.upper())
        filename.write("`define _%s_EnvTop_SV_\n" %self.tb_name.upper())
        filename.write("\n")
        filename.write("`include \"uvm_macros.svh\"\n")
        filename.write("\n")
        filename.write("package %s_EnvTop;\n"%self.tb_name)
        filename.write("\n")
        filename.write("\timport uvm_pkg::*;\n")
        filename.write("\t/** Import SVT UVM Package **/\n")
        svt_pkg=False
        for VipName in self.VIP_DB.keys():
            if self.VIP_DB[VipName]['Enable']:
                svt_pkg=True
        if svt_pkg==True:
            filename.write("\timport svt_uvm_pkg::*;\n")
        else:
            filename.write("\t//import svt_uvm_pkg::*;\n")

        # #if self.vip_apb_enable:
        # if self.VIP_DB['APB']['Enable']:
        #     filename.write("\timport svt_apb_uvm_pkg::*;\n")
        # #if self.vip_ahb_enable:
        # if self.VIP_DB['AHB']['Enable']:
        #     filename.write("\timport svt_ahb_uvm_pkg::*;\n")
        # #if self.vip_axi_enable:
        # if self.VIP_DB['AXI']['Enable']:
        #     filename.write("\timport svt_axi_uvm_pkg::*;\n")
        for VipName in self.VIP_DB.keys():
            if self.VIP_DB[VipName]['Enable']:
                filename.write("\timport svt_%s_uvm_pkg::*;\n"%VipName.lower())
        filename.write("\n")
        filename.write("\t/** Import the custom config UVC Package **/\n")
        for i in range(len(self.DUT_GroupName)):
            if self.DUT_VIP[i]==True:
                filename.write("\t`ifndef NO_%s_VIP\n"%self.DUT_GroupName[i])
                filename.write("\t  import %s_UvcTop::*;\n"%self.DUT_GroupName[i].lower())
                filename.write("\t`endif\n")
                filename.write("\n")
                filename.write("\t`ifndef NO_%s_CUSTOM\n"%self.DUT_GroupName[i])
                filename.write("\t  import %s_UvcTop::*;\n"%self.DUT_GroupName[i])
                filename.write("\t`endif\n")
        filename.write("\n")
        for i in range(len(self.DUT_GroupName)):
            if self.DUT_VIP[i]==False:
                filename.write("\timport %s_UvcTop::*;\n"%self.DUT_GroupName[i])
        filename.write("\n")
        filename.write("\ttypedef class %s_config;\n"%self.tb_name)
        filename.write("\ttypedef class %s_event;\n"%self.tb_name)
        filename.write("\ttypedef class %s_scoreboard;\n"%self.tb_name)
        filename.write("\ttypedef class %s_virtual_sequencer;\n"%self.tb_name)
        filename.write("\ttypedef class %s_env;\n"%self.tb_name)
        filename.write("\n")
        filename.write("\t`include \"%s_config.sv\"\n"%self.tb_name)
        filename.write("\t`include \"%s_event.sv\"\n"%self.tb_name)
        filename.write("\t`include \"%s_scoreboard.sv\"\n"%self.tb_name)
        filename.write("\t`include \"%s_virtual_sequencer.sv\"\n"%self.tb_name)
        filename.write("\t`include \"%s_env.sv\"\n"%self.tb_name)

        # ===== Register Model =====
        # 自动检测：若 Excel 中有寄存器定义，则 include regmodel 文件到 package
        self.reg_model_enable = hasattr(self, 'REG_Name') and len(self.REG_Name) > 0
        if self.reg_model_enable:
            filename.write("\t`include \"%s_reg_adapter.sv\"\n"%self.tb_name)
            filename.write("\t`include \"%s_reg_block.sv\"\n"%self.tb_name)

        filename.write("\n")
        filename.write("endpackage\n")
        filename.write("`endif\n")
        filename.close()

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")

    # def ExtractArray(self,sheetname,ExtractKeyword):
    #     ExtractKeywordName=[]
    #     for name in sheetname:
    #         if (not name.value ==None)&(not name.value==ExtractKeyword):
    #             ExtractKeywordName.append(name.value)
    #     return ExtractKeywordName

    # def getFileEnable(self,TitleName,FileName,Enable):
    #     for filename in TitleName:
    #         if filename.value == FileName:
    #             for EN in Enable:
    #                 if EN.row == filename.row:
    #                     enable=EN.value
    #     return enable
    
    # def getVipNum(self,VIP_name,VipName,VipNum):
    #     for vipname in VIP_name:
    #         if vipname.value == VipName:
    #             for vipnum in VipNum:
    #                 if vipnum.row == vipname.row:
    #                     Num=vipnum.value
    #     return Num

if __name__ == '__main__':
    gen=gen_env_EnvTop()