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
from gen_testcase.gen_xx_sequence_lib import gen_xx_sequence_lib
from gen_common.gen_common_task_fcuntion import gen_common_task_function
from common_lib.parameters import Parameters
from common_lib.common_lib import gen_uvm_body

class gen_testcase_sequence_lib:

    def __init__(self):
        print("[gen_testcase_sequencer_lib]:initial")
        #EnvironmentGenCfg='../VerifyEnvironmentGenCfg.xlsx'
        EnvironmentGenCfg=Parameters.EnvironmentGenCfg
        readexcel_WorkingDirectoryGen.readexcel_WorkingDirectoryGen_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_VIP.readexcel_VIP_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_ClockRst.readexcel_ClockRst_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_DutSignal.readexcel_DutSignal_info(self,EnvironmentGenCfg,PrintEnable=False)
        self.gen_testcase_sequence_lib_info(self.tb_name,PrintEnable=True)

    def gen_testcase_sequence_lib_info(self,name,PrintEnable):
        filename = open("%s_sequence_lib.sv"%name, "w+")
        filename.write("`ifndef _%s_SEQUENCE_LIB_SV_\n"%name.upper())
        filename.write("`define _%s_SEQUENCE_LIB_SV_\n"%name.upper())
        filename.write("\n")
        filename.write("class %s_virtual_seq_lib extends uvm_sequence;\n"%name)
        filename.write("\n")
        filename.write("\t%s_config     %s_cfg;\n"%(name,name))
        filename.write("\t%s_event      %s_evt;\n"%(name,name))
        filename.write("\n")
        
        # #vip
        # #if self.vip_apb_enable:
        # if self.VIP_DB['APB']['Enable']:
        #     #for i in range(0,self.VIP_apb_master_num):
        #     for i in range(self.VIP_DB['APB']['VipMasterNum']):
        #         filename.write("\t apb_master_wr_directed_sequence    apb_m_wr_seq%s;\n"%i)
        #         filename.write("\t apb_master_rd_directed_sequence    apb_m_rd_seq%s;\n"%i)
        #     #for i in range(0,self.VIP_apb_slave_num):
        #     for i in range(self.VIP_DB['APB']['VipSlaveNum']):
        #         filename.write("\t apb_slave_wr_directed_sequence     apb_s_wr_seq%s;\n"%i)
        #         filename.write("\t apb_slave_rd_directed_sequence     apb_s_rd_seq%s;\n"%i)
        # filename.write("\n")
        # #if self.vip_ahb_enable:
        # if self.VIP_DB['AHB']['Enable']:
        #     #for i in range(0,self.VIP_ahb_master_num):
        #     for i in range(self.VIP_DB['AHB']['VipMasterNum']):
        #         filename.write("\t ahb_master_wr_directed_sequence    ahb_m_wr_seq%s;\n"%i)
        #         filename.write("\t ahb_master_rd_directed_sequence    ahb_m_rd_seq%s;\n"%i)
        #     #for i in range(0,self.VIP_ahb_slave_num):
        #     for i in range(self.VIP_DB['AHB']['VipSlaveNum']):
        #         filename.write("\t ahb_slave_wr_directed_sequence     ahb_s_wr_seq%s;\n"%i)
        #         filename.write("\t ahb_slave_rd_directed_sequence     ahb_s_rd_seq%s;\n"%i)
        # filename.write("\n")
        # #if self.vip_axi_enable:
        # if self.VIP_DB['AXI']['Enable']:
        #     #for i in range(0,self.VIP_axi_master_num):
        #     for i in range(self.VIP_DB['AXI']['VipMasterNum']):
        #         filename.write("\t axi_master_wr_directed_sequence    axi_m_wr_seq%s;\n"%i)
        #         filename.write("\t axi_master_rd_directed_sequence    axi_m_rd_seq%s;\n"%i)
        #     #for i in range(0,self.VIP_axi_slave_num):
        #     for i in range(self.VIP_DB['APB']['VipSlaveNum']):
        #         filename.write("\t axi_slave_wr_directed_sequence     axi_s_wr_seq%s;\n"%i)
        #         filename.write("\t axi_slave_rd_directed_sequence     axi_s_rd_seq%s;\n"%i)
        # filename.write("\n")
        for VipName in self.VIP_DB.keys():
            if self.VIP_DB[VipName]['Enable']:
                vipname=VipName.lower()
                for i in range(self.VIP_DB[VipName]['VipMasterNum']):
                    filename.write("\t %s_master_wr_directed_seq    %s_m_wr_seq%s;\n"%(vipname,vipname,i))
                    filename.write("\t %s_master_rd_directed_seq    %s_m_rd_seq%s;\n"%(vipname,vipname,i))
                # for i in range(self.VIP_DB[VipName]['VipSlaveNum']):
                #     filename.write("\t %s_slave_wr_directed_sequence     %s_s_wr_seq%s;\n"%(vipname,vipname,i))
                #     filename.write("\t %s_slave_rd_directed_sequence     %s_s_rd_seq%s;\n"%(vipname,vipname,i))
                filename.write("\n")

        filename.write("\t`uvm_object_utils_begin(%s_virtual_seq_lib)\n"%name)
        filename.write("\t`uvm_object_utils_end\n")
        filename.write("\n")
        filename.write("\t`uvm_declare_p_sequencer(%s_virtual_sequencer)\n"%name)
        filename.write("\n")
        filename.write("\tfunction new(string name=\"%s_virtual_seq_lib\");\n"%name)
        filename.write("\t\tsuper.new(name);\n")
        filename.write("\t\t%s_cfg=new();\n"%name)
        filename.write("\t\t%s_evt=new();\n"%name)
        filename.write("\t\tset_automatic_phase_objection(1);\n")
        # filename.write("\t\tuvm_config_db#(%s_config)::set(null,\"*\",\"%s_config\",%s_cfg);\n"%(name,name,name))
        # filename.write("\t\tuvm_config_db#(%s_event)::set(null,\"*\",\"%s_event\",%s_evt);\n"%(name,name,name))
        filename.write("\tendfunction\n")
        filename.write("\n")
        
        # filename.write("\tvirtual task pre_body();\n")
        # filename.write("\t\t`uvm_info(get_full_name(),\"pre_body begin ...\",UVM_LOW)\n")
        # filename.write("\n")
        # filename.write("\t\tif(starting_phase !=null)\n")
        # filename.write("\t\t\tstarting_phase.raise_objection(this,\"virtual sequence raise_objection\");\n")
        # filename.write("\n")
        # filename.write("\t\tif(!uvm_config_db#(%s_config)::get(null,get_full_name(),\"%s_config\",%s_cfg))\n"%(name,name,name))
        # filename.write("\t\t\t`uvm_fatal(get_type_name(),\"Can't get config object!\")\n")
        # filename.write("\n")
        # filename.write("\t\tif(!uvm_config_db#(%s_event)::get(null,get_full_name(),\"%s_event\",%s_evt))\n"%(name,name,name))
        # filename.write("\t\t\t`uvm_fatal(get_type_name(),\"Can't get event object!\")\n")
        # filename.write("\n")
        # filename.write("\t\t`uvm_info(get_full_name(),\"pre_body end ...\",UVM_LOW)\n")
        # filename.write("\tendtask\n")
        # filename.write("\n")
        StrStr=[]
        StrStr.append("//%s_virtual_sequencer  mseqr;"%name)
        StrStr.append("//$cast(mseqr,m_sequencer);")
        StrStr.append("")
        StrStr.append("if(starting_phase !=null)")
        StrStr.append("\tstarting_phase.raise_objection(this,\"virtual sequence raise_objection\");")
        StrStr.append("")
        StrStr.append("if(!uvm_config_db#(%s_config)::get(null,get_full_name(),\"%s_config\",%s_cfg))"%(name,name,name))
        StrStr.append("\t`uvm_fatal(get_type_name(),\"Can't get config object!\")")
        StrStr.append("")
        StrStr.append("if(!uvm_config_db#(%s_event)::get(null,get_full_name(),\"%s_event\",%s_evt))"%(name,name,name))
        StrStr.append("\t`uvm_fatal(get_type_name(),\"Can't get event object!\")")
        StrStr.append("")
        gen_uvm_body(self,filename,'pre_body'               ,StrStr,Parameters.PrintEnable)

        # filename.write("\tvirtual task body();\n")
        # filename.write("\t\t`uvm_info(get_full_name(),\"body begin ...\",UVM_LOW)\n")
        # filename.write("\t\t//@(xx.rst)\n")
        # filename.write("\t\t`uvm_info(get_full_name(),\"body end ...\",UVM_LOW)\n")
        # filename.write("\tendtask\n")
        # filename.write("\n")
        gen_uvm_body(self,filename,'body'               ,None,Parameters.PrintEnable)

        # filename.write("\tvirtual task post_body();\n")
        # filename.write("\t\t`uvm_info(get_full_name(),\"post_body begin ...\",UVM_LOW)\n")
        # filename.write("\n")
        # filename.write("\t\tif(starting_phase !=null)\n")
        # filename.write("\t\t\tstarting_phase.drop_objection(this,\"virtual sequence drop_objection\");\n")
        # filename.write("\n")
        # filename.write("\t\t//@(xx.rst)\n")
        # filename.write("\t\t`uvm_info(get_full_name(),\"post_body end ...\",UVM_LOW)\n")
        # filename.write("\tendtask\n")
        # filename.write("\n")
        StrStr=[]
        StrStr.append("if(starting_phase!=null)")
        StrStr.append("\tstarting_phase.drop_objection(this);")
        StrStr.append("")
        gen_uvm_body(self,filename,'post_body'               ,StrStr,Parameters.PrintEnable)

        # #VIP sequence
        # filename.write("\t//VIP sequence\n")
        # #if self.vip_apb_enable:
        # if self.VIP_DB['APB']['Enable']:
        #     filename.write("\t`include\"apb_sequence_lib\"\n")
        #     #gen_apb_sequence_lib.sv
        # #if self.vip_ahb_enable:
        # if self.VIP_DB['AHB']['Enable']:
        #     filename.write("\t`include\"ahb_sequence_lib\"\n")
        #     #gen_ahb_sequence_lib.sv
        # #if self.vip_axi_enable:
        # if self.VIP_DB['AXI']['Enable']:
        #     filename.write("\t`include\"axi_sequence_lib\"\n")
        #     #gen_axi_sequence_lib.sv
        for VipName in self.VIP_DB.keys():
            if self.VIP_DB[VipName]['Enable']:
                filename.write("\t`include \"%s_common_task_function.sv\"\n"%VipName.lower())
                gen_xx_sequence_lib.gen_xx_common_task_funciton_info(self,VipName,PrintEnable=False)
                filename.write("\n")

         #common_task_function.sv
        filename.write("\n")
        filename.write("\t//your task or function\n")
        filename.write("\t`include \"%s_common_task_function.sv\"\n"%name)
        gen_common_task_function.gen_common_task_function_info(self,name,PrintEnable=True)
        filename.write("\n")
        filename.write("endclass\n")
        filename.write("\n")
        filename.write("`endif\n")
        filename.close()
        

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")
            
if __name__ == '__main__':
    gen=gen_testcase_sequence_lib()