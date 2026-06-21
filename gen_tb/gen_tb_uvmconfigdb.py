#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from readexcel.readexcel_WorkingDirectoryGen import readexcel_WorkingDirectoryGen
from readexcel.readexcel_DutSignal import readexcel_DutSignal
from readexcel.readexcel_ClockRst import readexcel_ClockRst
from common_lib.parameters import Parameters

class gen_tb_uvmconfigdb:

    def __init__(self):
        print("[gen_tb_uvmconfigdb]:initial")
        #EnvironmentGenCfg='../VerifyEnvironmentGenCfg.xlsx'
        EnvironmentGenCfg=Parameters.EnvironmentGenCfg
        readexcel_WorkingDirectoryGen.readexcel_WorkingDirectoryGen_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_DutSignal.readexcel_DutSignal_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_ClockRst.readexcel_ClockRst_info(self,EnvironmentGenCfg,PrintEnable=False)
        self.gen_tb_uvmconfigdb_info(None,self.tb_name,self.DUT_GroupName,self.Clk_name,self.Rst_name,PrintEnable=True)

    def gen_tb_uvmconfigdb_info(self,FileName,tb_name,DUT_GroupName,Clk_name,Rst_name,PrintEnable):
        if FileName==None:
            filename = open('uvmconfigdb.sv', "w+")
        else:
            filename=FileName

        vifvif=[]
        novipvip=[]
        vipvip=[]

        for i in range(0,len(DUT_GroupName)):
            GroupName=DUT_GroupName[i]
            if self.DUT_VIP[i]==False:
                novipvip.append("uvm_config_db#(virtual %s_vif)::set(null,\"*\",\"%s_vif\",TopVif.%svif);"%(GroupName,GroupName,GroupName))
                vifvif.append(GroupName)
            else:
                vipvip.append("")
                vipvip.append("`ifndef NO_%s_CUSTOM"%GroupName)
                vipvip.append("uvm_config_db#(virtual %s_vif)::set(null,\"*\",\"%s_vif\",TopVif.%svif);"%(GroupName,GroupName,GroupName))
                vipvip.append("`endif")
                vipvip.append("")
                vipvip.append("`ifndef NO_%s_VIP"%GroupName)
                if GroupName.lower()=="apb":
                    # vipvip.append("uvm_config_db#(virtual svt_apb_if)::set(null,\"*\",\"apb_vif\",apb_vip_vif);")
                    for i in range(self.VIP_DB['APB']['VipMasterNum']):
                        vipvip.append("uvm_config_db#(virtual svt_apb_if)::set(null,\"*\",\"apb_master%s_vif\",apb_master%s_vif);"%(i,i))
                    for i in range(self.VIP_DB['APB']['VipSlaveNum']):
                        vipvip.append("uvm_config_db#(virtual svt_apb_slave_if)::set(null,\"*\",\"apb_slave%s_vif\",apb_slave%s_vif);"%(i,i))
                if GroupName.lower()=="ahb":
                    vipvip.append("uvm_config_db#(virtual svt_ahb_if)::set(null,\"*\",\"ahb_vif\",ahb_vip_vif);")
                if GroupName.lower()=="axi":
                    vipvip.append("uvm_config_db#(virtual svt_axi_if)::set(null,\"*\",\"axi_vif\",axi_vip_vif);")
                vipvip.append("`endif")
        filename.write("\n")
        # for i in range(len(vifvif)):
        #     filename.write("virtual %s_vif  %svif;\n"%(vifvif[i],vifvif[i]))
        filename.write("\n")
        filename.write("typedef virtual %s_vif  %svif;\n"%(tb_name,tb_name))
        filename.write("%s_vif   TopVif(tb_top.%s,tb_top.%s);\n"%(tb_name,Clk_name[0],Rst_name[0]))
        filename.write("\n")
        for i in range(0,len(DUT_GroupName)):
            GroupName=DUT_GroupName[i]
            if self.DUT_VIP[i]==True:
                filename.write("reg %s_clk;\n"%GroupName.lower())
                filename.write("reg %s_rst;\n"%GroupName.lower())
        filename.write("\n")        
        for i in range(0,len(DUT_GroupName)):
            GroupName=DUT_GroupName[i]
            if self.DUT_VIP[i]==True:
                filename.write("`ifndef NO_%s_VIP\n"%GroupName)
                #apb
                if GroupName.lower()=="apb":
                    # filename.write("svt_apb_if  apb_vip_vif();\n")
                    # filename.write("\n")
                    # filename.write("assign apb_vip_vif.common_clk=apb_clk;\n")
                    # for i in range(self.VIP_DB['APB']['VipMasterNum']):
                    #     filename.write("assign apb_vip_vif.master_if[%s].pclk      =apb_clk;\n"%i)
                    #     filename.write("assign apb_vip_vif.master_if[%s].presetn   =apb_rst;\n"%i)
                    # filename.write("\n")
                    # for i in range(self.VIP_DB['APB']['VipSlaveNum']):
                    #     filename.write("assign apb_vip_vif.slave_if[%s].pclk       =apb_clk;\n"%i)
                    #     filename.write("assign apb_vip_vif.slave_if[%s].presetn    =apb_rst;\n"%i)
                    for i in range(self.VIP_DB['APB']['VipMasterNum']):
                        filename.write("svt_apb_if  apb_master%s_vif();\n"%i)
                        filename.write("//assign apb_master%s_vif.common_clk=apb_clk;\n"%i)
                        filename.write("assign apb_master%s_vif.pclk      =apb_clk;\n"%i)
                        filename.write("assign apb_master%s_vif.presetn   =apb_rst;\n"%i)
                    filename.write("\n")
                    for i in range(self.VIP_DB['APB']['VipSlaveNum']):
                        filename.write("svt_apb_slave_if  apb_slave%s_vif();\n"%i)
                        filename.write("//assign apb_slave%s_vif.common_clk=apb_clk;\n"%i)
                        filename.write("assign apb_slave%s_vif.pclk      =apb_clk;\n"%i)
                        filename.write("assign apb_slave%s_vif.presetn   =apb_rst;\n"%i)
                #ahb
                if GroupName.lower()=="ahb":
                    filename.write("svt_apb_if  ahb_vip_vif();\n")
                    filename.write("\n")
                    filename.write("assign ahb_vip_vif.common_clk=ahb_clk;\n")
                    for i in range(self.VIP_DB['AHB']['VipMasterNum']):
                        filename.write("assign ahb_vip_vif.master_if[%s].hclk      =ahb_clk;\n"%i)
                        filename.write("assign ahb_vip_vif.master_if[%s].hresetn   =ahb_rst;\n"%i)
                    filename.write("\n")
                    for i in range(self.VIP_DB['AHB']['VipSlaveNum']):
                        filename.write("assign ahb_vip_vif.slave_if[%s].hclk       =ahb_clk;\n"%i)
                        filename.write("assign ahb_vip_vif.slave_if[%s].hresetn    =ahb_rst;\n"%i)
                #axi
                if GroupName.lower()=="axi":
                    filename.write("svt_apb_if  axi_vip_vif();\n")
                    filename.write("\n")
                    filename.write("assign axi_vip_vif.common_clk=axi_clk;\n")
                    for i in range(self.VIP_DB['AXI']['VipMasterNum']):
                        filename.write("assign axi_vip_vif.master_if[%s].aclk      =axi_clk;\n"%i)
                        filename.write("assign axi_vip_vif.master_if[%s].aresetn   =axi_rst;\n"%i)
                    filename.write("\n")
                    for i in range(self.VIP_DB['AXI']['VipSlaveNum']):
                        filename.write("assign axi_vip_vif.slave_if[%s].aclk       =axi_clk;\n"%i)
                        filename.write("assign axi_vip_vif.slave_if[%s].aresetn    =axi_rst;\n"%i)
                filename.write("`endif\n")
        filename.write("\n")
        filename.write("//You must check whether the virtual interface is declared and its correctness!!!\n")
        filename.write("initial begin\n")
        #filename.write("\tuvm_config_db#(virtual %s_vif)::set(null,\"*\",\"%s_vif\",%svif);\n"%(tb_name,tb_name,tb_name))
        filename.write("\tuvm_config_db#(virtual %s_vif)::set(null,\"*\",\"%s_vif\",TopVif);\n"%(tb_name,tb_name))
        filename.write("\n")
        for i in range(len(novipvip)):
            filename.write("\t%s\n"%novipvip[i])
        filename.write("\n")
        for i in range(len(vipvip)):
            filename.write("\t%s\n"%vipvip[i])
        filename.write("\n")
        filename.write("\trun_test();\n")
        filename.write("\n")
        filename.write("end\n")
        filename.write("\n")
        filename.write("//Write the assertions of the tb_top layer in the following file and open the corresponding macro definition\n")
        filename.write("`ifdef SVA_TB_TOP\n")
        filename.write("\t`include\"./../sva/code/sva_tb_top.sv\"\n")
        filename.write("`endif\n")
 
        if FileName==None:
            filename.close()

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")
    
if __name__ == '__main__':
    gen=gen_tb_uvmconfigdb()