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
from common_lib.common_lib import gen_uvm_new
from common_lib.common_lib import gen_uvm_phase

class gen_env_virtual_sequencer:

    def __init__(self):
        print("[gen_env_EnvTop]:initial")
        #EnvironmentGenCfg='../VerifyEnvironmentGenCfg.xlsx'
        EnvironmentGenCfg=Parameters.EnvironmentGenCfg
        readexcel_WorkingDirectoryGen.readexcel_WorkingDirectoryGen_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_VIP.readexcel_VIP_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_ClockRst.readexcel_ClockRst_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_DutSignal.readexcel_DutSignal_info(self,EnvironmentGenCfg,PrintEnable=False)
        self.gen_env_virtual_sequencer_info(PrintEnable=True)

    def gen_env_virtual_sequencer_info(self,PrintEnable):
        filename = open("%s_virtual_sequencer.sv"%self.tb_name, "w+")
        filename.write("`ifndef _%s_VIRTUAL_SEQUENCER_SV_\n" %self.tb_name.upper())
        filename.write("`define _%s_VIRTUAL_SEQUENCER_SV_\n" %self.tb_name.upper())
        filename.write("\n")
        filename.write("class %s_virtual_sequencer extends uvm_sequencer;\n" %self.tb_name)
        filename.write("\n")
        filename.write("\t%s_config    sct_cfg;\n"%self.tb_name)
        filename.write("\n")
        
        #[1]:Declare all sequencer
        # # apb vip sequencer
        # #if self.vip_apb_enable:
        # if self.VIP_DB['APB']['Enable']:
        #     #for i in range(self.VIP_apb_master_num):
        #     for i in range(self.VIP_DB['APB']['VipMasterNum']):
        #         filename.write("\tsvt_apb_master_sequencer     apb_master_seqr_%s;\n"%i) 
        #     #for i in range(self.VIP_apb_slave_num):
        #     for i in range(self.VIP_DB['APB']['VipSlaveNum']):
        #         filename.write("\tsvt_apb_slave_sequencer      apb_slave_seqr_%s;\n"%i) 
        # filename.write("\n")
        
        # # ahb vip sequencer
        # #if self.vip_ahb_enable:
        # if self.VIP_DB['AHB']['Enable']:
        #     #for i in range(self.VIP_ahb_master_num):
        #     for i in range(self.VIP_DB['AHB']['VipMasterNum']):
        #         filename.write("\tsvt_ahb_master_sequencer     ahb_master_seqr_%s;\n"%i) 
        #     #for i in range(self.VIP_ahb_slave_num):
        #     for i in range(self.VIP_DB['AHB']['VipSlaveNum']):
        #         filename.write("\tsvt_ahb_slave_sequencer      ahb_slave_seqr_%s;\n"%i) 
        # filename.write("\n")
        
        # # axi vip sequencer
        # #if self.vip_axi_enable:
        # if self.VIP_DB['AXI']['Enable']:
        #     #for i in range(self.VIP_axi_master_num):
        #     for i in range(self.VIP_DB['AXI']['VipMasterNum']):
        #         filename.write("\tsvt_axi_master_sequencer     axi_master_seqr_%s;\n"%i) 
        #     #for i in range(self.VIP_axi_slave_num):
        #     for i in range(self.VIP_DB['AXI']['VipSlaveNum']):
        #         filename.write("\tsvt_axi_slave_sequencer      axi_slave_seqr_%s;\n"%i) 
        # filename.write("\n")
        for VipName in self.VIP_DB.keys():
            if self.VIP_DB[VipName]['Enable']:
                vipname=VipName.lower()
                # for i in range(self.VIP_DB[VipName]['VipMasterNum']):
                #     filename.write("\tsvt_%s_master_sequencer     %s_master_seqr_%s;\n"%(vipname,vipname,i)) 
                # for i in range(self.VIP_DB[VipName]['VipSlaveNum']):
                #     filename.write("\tsvt_%s_slave_sequencer      %s_slave_seqr_%s;\n"%(vipname,vipname,i))
                filename.write("\t`ifndef NO_%s_VIP\n"%VipName)
                if(VipName=='APB'):
                    for i in range(self.VIP_DB[VipName]['VipMasterNum']):
                        filename.write("\tsvt_apb_system_sequencer     %s_master_seqr_%s;\n"%(vipname,i)) 
                    for i in range(self.VIP_DB[VipName]['VipSlaveNum']):
                        filename.write("\tsvt_apb_system_sequencer    %s_slave_seqr_%s;\n"%(vipname,i))
                if(VipName=='AHB'):
                    for i in range(self.VIP_DB[VipName]['VipMasterNum']):
                        filename.write("\tsvt_ahb_master_transaction_sequencer  %s_master_seqr_%s;\n"%(vipname,i)) 
                    # for i in range(self.VIP_DB[VipName]['VipSlaveNum']):
                    #     filename.write("\tsvt_ahb_slave_transaction_sequencer   %s_slave_seqr_%s;\n"%(vipname,vipname,i))
                if(VipName=='AXI'):
                    for i in range(self.VIP_DB[VipName]['VipMasterNum']):
                        filename.write("\tsvt_axi_master_sequencer     axi_master_seqr_%s;\n"%i) 
                    for i in range(self.VIP_DB[VipName]['VipSlaveNum']):
                        filename.write("\tsvt_axi_slave_sequencer      axi_slave_seqr_%s;\n"%i)
                filename.write("\t`endif\n")
                filename.write("\n") 
        
        #uvc sequencer
        for i in range(len(self.DUT_GroupName)):
            if self.DUT_VIP[i]==False:
                filename.write("\t%s_sequencer         %s_seqr;\n"%(self.DUT_GroupName[i],self.DUT_GroupName[i]))
            else:
                filename.write("\t`ifndef NO_%s_CUSTOM\n"%self.DUT_GroupName[i])
                filename.write("\t%s_sequencer         %s_seqr;\n"%(self.DUT_GroupName[i],self.DUT_GroupName[i]))
                filename.write("\t`endif\n")

        filename.write("\n")
        # parameters of json
        filename.write("\t//You can add some parameters that you want to pass through the json table here;\n")
        filename.write("\trand bit[1:0]aa;\n") 
        filename.write("\tstring       bb;\n") 
        
        #[2]:Register all sequencer
        filename.write("\t`uvm_component_utils_begin(%s_virtual_sequencer)\n"%self.tb_name)
        filename.write("\n")
        
        # #  apb vip sequencer
        # #if self.vip_apb_enable:
        # if self.VIP_DB['APB']['Enable']:
        #     #for i in range(self.VIP_apb_master_num):
        #     for i in range(self.VIP_DB['APB']['VipMasterNum']):
        #         filename.write("\t\t`uvm_field_object(apb_master_seqr_%s,UVM_ALL_ON);\n"%i)
        #     #for i in range(self.VIP_apb_slave_num):
        #     for i in range(self.VIP_DB['APB']['VipSlaveNum']):
        #         filename.write("\t\t`uvm_field_object(apb_slave_seqr_%s,UVM_ALL_ON);\n"%i)
        # filename.write("\n")
        
        # #  apb vip sequencer
        # #if self.vip_ahb_enable:
        # if self.VIP_DB['AHB']['Enable']:
        #     #for i in range(self.VIP_ahb_master_num):
        #     for i in range(self.VIP_DB['AHB']['VipMasterNum']):
        #         filename.write("\t\t`uvm_field_object(ahb_master_seqr_%s,UVM_ALL_ON);\n"%i)
        #     #for i in range(self.VIP_ahb_slave_num):
        #     for i in range(self.VIP_DB['AHB']['VipSlaveNum']):
        #         filename.write("\t\t`uvm_field_object(ahb_slave_seqr_%s,UVM_ALL_ON);\n"%i)
        # filename.write("\n")
        
        # #  axi vip sequencer
        # #if self.vip_axi_enable:
        # if self.VIP_DB['AXI']['Enable']:
        #     #for i in range(self.VIP_axi_master_num):
        #     for i in range(self.VIP_DB['AXI']['VipMasterNum']):
        #         filename.write("\t\t`uvm_field_object(axi_master_seqr_%s,UVM_ALL_ON);\n"%i)
        #     #for i in range(self.VIP_axi_slave_num):
        #     for i in range(self.VIP_DB['AXI']['VipSlaveNum']):
        #         filename.write("\t\t`uvm_field_object(axi_slave_seqr_%s,UVM_ALL_ON);\n"%i)
        # filename.write("\n")
        for VipName in self.VIP_DB.keys():
            if self.VIP_DB[VipName]['Enable']:
                vipname=VipName.lower()
                filename.write("\t`ifndef NO_%s_VIP\n"%VipName)
                for i in range(self.VIP_DB[VipName]['VipMasterNum']):
                    filename.write("\t\t`uvm_field_object(%s_master_seqr_%s,UVM_ALL_ON);\n"%(vipname,i)) 
                for i in range(self.VIP_DB[VipName]['VipSlaveNum']):
                    filename.write("\t\t`uvm_field_object(%s_slave_seqr_%s,UVM_ALL_ON);\n"%(vipname,i)) 
                filename.write("\t`endif\n")

        #uvc sequencer
        for i in range(len(self.DUT_GroupName)):
            if self.DUT_VIP[i]==False:
                filename.write("\t\t`uvm_field_object(%s_seqr,UVM_ALL_ON);\n"%self.DUT_GroupName[i])
            else:
                filename.write("\t`ifndef NO_%s_CUSTOM\n"%self.DUT_GroupName[i])
                filename.write("\t\t`uvm_field_object(%s_seqr,UVM_ALL_ON);\n"%self.DUT_GroupName[i])
                filename.write("\t`endif\n")

        filename.write("\n")
        # parameters of json
        filename.write("\t\t//parameters of json\n")
        filename.write("\t\t`uvm_field_int(aa,UVM_ALL_ON);\n")
        filename.write("\t\t`uvm_field_string(bb,UVM_ALL_ON);\n")
        filename.write("\n")
        filename.write("\t`uvm_field_utils_end\n")
        filename.write("\n")
        # filename.write("\tfunction new(string name=\"%s_virtual_sequencer\",uvm_component parent=null);\n"%self.tb_name)
        # filename.write("\t\tsuper.new(name,parent);\n")
        # filename.write("\tendfunction\n")
        gen_uvm_new(self,filename,'%s_virtual_sequencer'%self.tb_name,'uvm_component',None,Parameters.PrintEnable)

        gen_uvm_phase(self,filename,'build_phase'               ,None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'connect_phase'             ,None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'end_of_elaboration_phase'  ,None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'start_of_simulation_phase' ,None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'run_phase'                 ,None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'extract_phase'             ,None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'check_phase'               ,None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'report_phase'              ,None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'final_phase'               ,None,Parameters.PrintEnable)

        # filename.write("\n")
        # filename.write("\tvirtual function void build_phase(uvm_phase phase);\n")
        # filename.write("\t\tsuper.build_phase(phase);\n")
        # filename.write("\tendfunction\n")
        # filename.write("\n")

        filename.write("endclass\n")
        filename.write("\n")
        filename.write("`endif\n")
        filename.write("\n")
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
    gen=gen_env_virtual_sequencer()