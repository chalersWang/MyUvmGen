#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os
import sys
import operator
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# from readexcel.readexcel_WorkingDirectoryGen import readexcel_WorkingDirectoryGen
from readexcel.readexcel_VIP import readexcel_VIP
# from readexcel.readexcel_DutSignal import readexcel_DutSignal
# from readexcel.readexcel_ClockRst import readexcel_Clock Rst
from common_lib.parameters import Parameters

class gen_ahb_uvc:

    def __init__(self):
        print("[gen_xx_sequence_lib]:initial")
        #EnvironmentGenCfg='../VerifyEnvironmentGenCfg.xlsx'
        EnvironmentGenCfg=Parameters.EnvironmentGenCfg
        # readexcel_WorkingDirectoryGen.readexcel_WorkingDirectoryGen_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_VIP.readexcel_VIP_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_VIP.readexcel_VIP_AXI_info(self,EnvironmentGenCfg,PrintEnable=False)
        # readexcel_ClockRst.readexcel_ClockRst_info(self,EnvironmentGenCfg,PrintEnable=False)
        # readexcel_DutSignal.readexcel_DutSignal_info(self,EnvironmentGenCfg,PrintEnable=False)
        self.gen_ahb_uvc_info(PrintEnable=False)
        

    def gen_ahb_uvc_info(self,PrintEnable):
        #############################ahb_UvcTop.svh########################################################
        filename = open("ahb_UvcTop.svh", "w+")
        filename.write("`ifndef _AHB_UVC_TOP_SVH\n")
        filename.write("`define _AHB_UVC_TOP_SVH\n")
        filename.write("\n")
        filename.write("`include \"uvm_macros.svh\"\n")
        filename.write("\n")
        filename.write("package ahb_UvcTop;\n")
        filename.write("\timport uvm_pkg::*;\n")
        filename.write("\n")
        filename.write("\t/** Import the SVT UVM PKG **/\n")
        filename.write("\timport svt_uvm_pkg::*;\n")
        filename.write("\n")
        filename.write("\t/** Import the AHB VIP **/\n")
        filename.write("\timport svt_ahb_uvm_pkg::*;\n")
        filename.write("\n")
        filename.write("\ttypedef class ahb_cust_config;\n")
        filename.write("\ttypedef class ahb_base_seq;\n")
        filename.write("\n")
        filename.write("\t`include \"ahb_cust_config.sv\";\n")
        filename.write("\t`include \"ahb_sequence_lib.sv\";\n")
        filename.write("\n")
        filename.write("endpackage\n")
        filename.write("\n")
        filename.write("`endif\n")
        filename.close()
        #############################ahb_cust_config.sv########################################################
        filename = open("ahb_cust_config.sv", "w+")
        filename.write("`ifndef _AHB_CUST_CONFIG_SV\n")
        filename.write("`define _AHB_CUST_CONFIG_SV\n")
        filename.write("\n")
        filename.write("`define PRJ_AHB_NUM_MASTERS %s\n"%self.VIP_DB['AHB']['VipMasterNum'])
        filename.write("`define PRJ_AHB_NUM_SLAVES  %s\n"%self.VIP_DB['AHB']['VipSlaveNum'])
        filename.write("\n")
        filename.write("class ahb_cust_config extends uvm_object;\n")
        filename.write("    svt_ahb_system_configuration    ahb_cfg;\n")
        filename.write("\n")
        filename.write("    `uvm_object_utils_begin(ahb_cust_config)\n")
        filename.write("        `uvm_field_object(ahb_cfg,UVM_DEFAULT)\n")
        filename.write("    `uvm_object_utils_end\n")
        filename.write("\n")
        filename.write("    function new(string name=\"ahb_cust_config\");\n")
        filename.write("        super.new(name);\n")
        filename.write("\n")
        filename.write("        ahb_cfg=new(\"ahb_cfg\");\n")
        filename.write("\n")
        filename.write("        ahb_cfg.num_masters=`PRJ_AHB_NUM_MASTERS;\n")
        filename.write("        ahb_cfg.num_slaves =`PRJ_AHB_NUM_SLAVES;\n")
        filename.write("\n")
        filename.write("        //Create port configurations\n")
        filename.write("        ahb_cfg.create_sub_cfgs(`PRJ_AHB_NUM_MASTERS,`PRJ_AHB_NUM_SLAVES);\n")
        filename.write("        ahb_cfg.ahb_lite                =1;\n")
        filename.write("        ahb_cfg.system_monitor_enable   =1;\n")
        filename.write("        ahb_cfg.error_response_policy   =svt_ahb_system_configuration::CONTINUE_ON_ERROR;\n")
        filename.write("\n")
        for i in range(self.VIP_DB['AHB']['VipMasterNum']):
            MasterID="Master%s"%i
            filename.write("        // cfg of master%s\n"%i)
            filename.write("        ahb_cfg.master_cfg[%s].uvm_reg_enable              =1;\n"%i)
            filename.write("        ahb_cfg.master_cfg[%s].transaction_coverage_enable =0;\n"%i)
            filename.write("        ahb_cfg.master_cfg[%s].protocol_checks_enable      =1;\n"%i)
            filename.write("        ahb_cfg.master_cfg[%s].generate_hbstrb_and_hunalign=1;\n"%i)
            filename.write("        ahb_cfg.master_cfg[%s].is_active            =1;\n")
            filename.write("        ahb_cfg.master_cfg[%s].addr_width           =%s;\n"%(i,self.VIP_DB_Feature['AHB'][MasterID]['AddrWidth']))
            filename.write("        ahb_cfg.master_cfg[%s].data_width           =%s;\n"%(i,self.VIP_DB_Feature['AHB'][MasterID]['DataWidth']))
            filename.write("        ahb_cfg.master_cfg[%s].ahb_interface_type    =svt_ahb_configuration::AHB_V6;\n"%i)
            filename.write("\n")
        for i in range(self.VIP_DB['AHB']['VipSlaveNum']):
            SlaveID="Slave%s"%i
            filename.write("        // cfg of slave%s\n"%i)
            filename.write("        ahb_cfg.slave_cfg[%s].is_active             =1;\n")
            filename.write("        ahb_cfg.slave_cfg[%s].addr_width            =%s;\n"%(i,self.VIP_DB_Feature['AHB'][SlaveID]['AddrWidth']))
            filename.write("        ahb_cfg.slave_cfg[%s].data_width            =%s;\n"%(i,self.VIP_DB_Feature['AHB'][SlaveID]['DataWidth']))
            filename.write("\n")
        filename.write("    endfunction\n")
        filename.write("\n")
        filename.write("endclass\n")
        filename.write("\n")
        filename.write("`endif\n")
        filename.close()
        #############################axi_sequence_lib.sv########################################################
        filename = open("ahb_sequence_lib.sv", "w+")
        filename.write("`ifndef _AHB_SEQUENCE_LIB_SV\n")
        filename.write("`define _AHB_SEQUENCE_LIB_SV\n")
        filename.write("\n")
        # ahb_base_seq
        filename.write("class ahb_base_seq extends svt_ahb_master_transaction_base_sequence;\n")
        filename.write("\n")
        filename.write("    ahb_cust_config   ahb_cfg;\n")
        filename.write("\n")
        filename.write("    `uvm_object_utils_begin(ahb_base_seq)\n")
        filename.write("        `uvm_field_object(ahb_cfg,UVM_DEFAULT)\n")
        filename.write("    `uvm_object_utils_end\n")
        filename.write("\n")
        filename.write("    function new(string name=\"ahb_base_seq\");\n")
        filename.write("        super.new(name);\n")
        filename.write("    endfunction\n")
        filename.write("\n")
        filename.write("    virtual task pre_start();\n")
        filename.write("        //`uvm_info(get_full_name(),\"pre_start\",UVM_LOW)\n")
        filename.write("        if(starting_phase!=null)\n")
        filename.write("            starting_phase.raise_objection(this);\n")
        filename.write("    endtask\n")
        filename.write("\n")
        filename.write("    virtual task post_start();\n")
        filename.write("        //`uvm_info(get_full_name(),\"post_start\",UVM_LOW)\n")
        filename.write("        if(starting_phase!=null)\n")
        filename.write("            starting_phase.raise_objection(this);\n")
        filename.write("    endtask\n")
        filename.write("\n")
        filename.write("    virtual task body();\n")
        filename.write("        //`uvm_info(get_full_name(),\"body\",UVM_LOW)\n")
        filename.write("    endtask\n")
        filename.write("\n")
        filename.write("endclass\n")
        filename.write("\n")
        filename.write("`endif\n")
        filename.close()

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")
 
            
if __name__ == '__main__':
    gen=gen_ahb_uvc()