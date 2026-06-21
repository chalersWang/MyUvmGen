#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from readexcel.readexcel_DutSignal import readexcel_DutSignal
from readexcel.readexcel_ClockRst import readexcel_ClockRst
from readexcel.readexcel_WorkingDirectoryGen import readexcel_WorkingDirectoryGen
from readexcel.readexcel_VIP import readexcel_VIP

from .gen_tb_crg import gen_tb_crg
from .gen_tb_dutinst import gen_tb_dutinst
from .gen_tb_uvmconfigdb import gen_tb_uvmconfigdb
from .gen_tb_dumpctrl import gen_tb_dumpctrl

from common_lib.parameters import Parameters


class gen_tb_top:

    def __init__(self):
        print("[gen_tb_top]:initial")
        #EnvironmentGenCfg='../VerifyEnvironmentGenCfg.xlsx'
        EnvironmentGenCfg=Parameters.EnvironmentGenCfg
        readexcel_WorkingDirectoryGen.readexcel_WorkingDirectoryGen_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_VIP.readexcel_VIP_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_ClockRst.readexcel_ClockRst_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_DutSignal.readexcel_DutSignal_info(self,EnvironmentGenCfg,PrintEnable=False)
        self.gen_tb_top_info(self.tb_name,PrintEnable=True)

    def gen_tb_top_info(self,tb_name,PrintEnable):
        # tb_top.sv
        tb_top_filename="tb_top.sv"
        filename = open(tb_top_filename, "w+")

        filename.write("module tb_top;                          \n")
        filename.write("\n")
        filename.write("import uvm_pkg::*;\n")
        filename.write("\n")
        #filename.write("import svt_uvm_pkg::*;                  \n")
        svt_pkg=False
        for VipName in self.VIP_DB.keys():
            if self.VIP_DB[VipName]['Enable']:
                svt_pkg=True
        if svt_pkg==True:
            filename.write("import svt_uvm_pkg::*;\n")
        else:
            filename.write("//import svt_uvm_pkg::*;\n")

        #if self.vip_apb_enable:
        if self.VIP_DB['APB']['Enable']:
            filename.write("import svt_apb_uvm_pkg::*;          \n")
        #if self.vip_ahb_enable:
        if self.VIP_DB['AHB']['Enable']:
            filename.write("import svt_ahb_uvm_pkg::*;          \n")
        #if self.vip_axi_enable:
        if self.VIP_DB['AXI']['Enable']:
            filename.write("import svt_axi_uvm_pkg::*;          \n")
        filename.write("\n")
        filename.write("import %s_TestTop::*;                   \n" %tb_name)
        filename.write("\n")
        
        # #if self.vip_apb_enable:
        # if self.VIP_DB['APB']['Enable']:
        #     filename.write("reg apb_clk;                                        \n")
        #     filename.write("reg apb_rst;                                        \n")
        #     filename.write("svt_apb_if  apb_vif   ();                           \n")
        #     filename.write("assign apb_vif.pclk     =apb_clk;                   \n")
        #     filename.write("assign apb_vif.presetn  =apb_rst;                   \n")
        #     #for i in range(0,self.VIP_apb_master_num):
        #     for i in range(0,self.VIP_DB['APB']['VipMasterNum']):
        #         filename.write("assign apb_vif.master_if[%s].pclk    =apb_clk;  \n" %i)
        #         filename.write("assign apb_vif.master_if[%s].presetn =apb_rst;  \n" %i)
        #     #for i in range(0,self.VIP_apb_slave_num):
        #     for i in range(0,self.VIP_DB['APB']['VipSlaveNum']):
        #         filename.write("assign apb_vif.slave_if[%s].pclk     =apb_clk;  \n" %i)
        #         filename.write("assign apb_vif.slave_if[%s].presetn  =apb_rst;  \n" %i)
        # filename.write("\n")
        # #if self.vip_ahb_enable:
        # if self.VIP_DB['AHB']['Enable']:
        #     filename.write("reg ahb_clk;                                        \n")
        #     filename.write("reg ahb_rst;                                        \n")
        #     filename.write("svt_ahb_if  ahb_vif   ();                           \n")
        #     filename.write("assign ahb_vif.hclk     =ahb_clk;                   \n")
        #     filename.write("assign ahb_vif.hresetn  =ahb_rst;                   \n")
        #     #for i in range(0,self.VIP_ahb_master_num):
        #     for i in range(0,self.VIP_DB['AHB']['VipMasterNum']):
        #         filename.write("assign ahb_vif.master_if[%s].hclk    =ahb_clk;  \n" %i)
        #         filename.write("assign ahb_vif.master_if[%s].hresetn =ahb_rst;  \n" %i)
        #     #for i in range(0,self.VIP_ahb_slave_num):
        #     for i in range(0,self.VIP_DB['AHB']['VipSlaveNum']):
        #         filename.write("assign ahb_vif.slave_if[%s].pclk     =ahb_clk;  \n" %i)
        #         filename.write("assign ahb_vif.slave_if[%s].presetn  =ahb_rst;  \n" %i)
        # filename.write("\n")
        # #if self.vip_axi_enable:
        # if self.VIP_DB['AXI']['Enable']:
        #     filename.write("reg axi_clk;                                        \n")
        #     filename.write("reg axi_rst;                                        \n")
        #     filename.write("svt_axi_if  axi_vif   ();                           \n")
        #     filename.write("assign axi_vif.common_aclk =axi_clk;                \n")
        #     #for i in range(0,self.VIP_axi_master_num):
        #     for i in range(0,self.VIP_DB['AXI']['VipMasterNum']):
        #         filename.write("assign axi_vif.master_if[%s].aclk    =axi_clk;  \n" %i)
        #         filename.write("assign axi_vif.master_if[%s].aresetn =axi_rst;  \n" %i)
        #     #for i in range(0,self.VIP_axi_slave_num):
        #     for i in range(0,self.VIP_DB['AXI']['VipSlaveNum']):
        #         filename.write("assign axi_vif.slave_if[%s].aclk     =axi_clk;  \n" %i)
        #         filename.write("assign axi_vif.slave_if[%s].aresetn  =axi_rst;  \n" %i)
        # filename.write("\n")
        
        # crg_gen
        if self.crg_gen_sv_enable:
            filename.write("\n")
            filename.write("`include \"crg_gen.sv\"\n")
            filename.write("\n")
            #self.gen_crggen()
            gen_tb_crg.gen_tb_crg_info(self,None,self.Clk_name,self.Clk_period,self.Rst_name,self.Rst_release,PrintEnable=False)
        else:
            #self.gen_crggen()
            gen_tb_crg.gen_tb_crg_info(self,filename,self.Clk_name,self.Clk_period,self.Rst_name,self.Rst_release,PrintEnable=False)
         
        # uvmconfigdb
        if self.uvmconfigdb_sv_enable:
            filename.write("\n")
            filename.write("`include \"uvmconfigdb.sv\"   \n")
            filename.write("\n")
            #self.gen_uvmconfigdb()
            gen_tb_uvmconfigdb.gen_tb_uvmconfigdb_info(self,None,self.tb_name,self.DUT_GroupName,self.Clk_name,self.Rst_name,PrintEnable=False)
        else:
            #self.gen_uvmconfigdb()
            gen_tb_uvmconfigdb.gen_tb_uvmconfigdb_info(self,filename,self.tb_name,self.DUT_GroupName,self.Clk_name,self.Rst_name,PrintEnable=False)
        
        # dutinst
        if self.dutinst_sv_enable:
            filename.write("\n")
            filename.write("`include \"dutinst.sv\"  \n")
            filename.write("\n")
            #self.gen_dutinst()
            gen_tb_dutinst.gen_tb_dutinst_info(self,None,self.DUT_Name,self.DUT_GroupName,self.DUT_Signals,PrintEnable=False)
        else:
            #self.gen_dutinst()
            gen_tb_dutinst.gen_tb_dutinst_info(self,filename,self.DUT_Name,self.DUT_GroupName,self.DUT_Signals,PrintEnable=False)
        

        # dumpctrl
        if self.dumpctrl_sv_enable:
            filename.write("\n")
            filename.write("`include \"dumpctrl.sv\"\n")
            filename.write("\n")
            #self.gen_dumpctrl()
            gen_tb_dumpctrl.gen_tb_dumpctrl_info(self,None,PrintEnable=False)
        else:
            #self.gen_dumpctrl()
            gen_tb_dumpctrl.gen_tb_dumpctrl_info(self,filename,PrintEnable=False)

        filename.write("\n")
        filename.write("endmodule\n")
        filename.close()

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")

if __name__ == '__main__':
    gen=gen_tb_top()