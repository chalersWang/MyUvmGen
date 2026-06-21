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

class gen_apb_uvc:

    def __init__(self):
        print("[gen_xx_sequence_lib]:initial")
        #EnvironmentGenCfg='../VerifyEnvironmentGenCfg.xlsx'
        EnvironmentGenCfg=Parameters.EnvironmentGenCfg
        # readexcel_WorkingDirectoryGen.readexcel_WorkingDirectoryGen_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_VIP.readexcel_VIP_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_VIP.readexcel_VIP_AXI_info(self,EnvironmentGenCfg,PrintEnable=False)
        # readexcel_ClockRst.readexcel_ClockRst_info(self,EnvironmentGenCfg,PrintEnable=False)
        # readexcel_DutSignal.readexcel_DutSignal_info(self,EnvironmentGenCfg,PrintEnable=False)
        self.gen_apb_uvc_info(PrintEnable=False)
        

    def gen_apb_uvc_info(self,PrintEnable):
        #############################apb_UvcTop.svh########################################################
        filename = open("apb_UvcTop.svh", "w+")
        filename.write("`ifndef _APB_UVC_TOP_SVH\n")
        filename.write("`define _APB_UVC_TOP_SVH\n")
        filename.write("\n")
        filename.write("`include \"uvm_macros.svh\"\n")
        filename.write("\n")
        filename.write("package apb_UvcTop;\n")
        filename.write("\timport uvm_pkg::*;\n")
        filename.write("\n")
        filename.write("\t/** Import the SVT UVM PKG **/\n")
        filename.write("\timport svt_uvm_pkg::*;\n")
        filename.write("\n")
        filename.write("\t/** Import the AHB VIP **/\n")
        filename.write("\timport svt_apb_uvm_pkg::*;\n")
        filename.write("\n")
        filename.write("\ttypedef class apb_cust_config;\n")
        filename.write("\t//typedef class apb_base_seq;\n")
        filename.write("\n")
        filename.write("\t`include \"apb_cust_config.sv\";\n")
        filename.write("\t`include \"apb_sequence_lib.sv\";\n")
        filename.write("\n")
        filename.write("endpackage\n")
        filename.write("\n")
        filename.write("`endif\n")
        filename.close()
        #############################apb_cust_config.sv########################################################
        filename = open("apb_cust_config.sv", "w+")
        filename.write("`ifndef _APB_CUST_CONFIG_SV\n")
        filename.write("`define _APB_CUST_CONFIG_SV\n")
        filename.write("\n")
        # filename.write("`define PRJ_APB_NUM_MASTERS %s\n"%self.VIP_DB['APB']['VipMasterNum'])
        # filename.write("`define PRJ_APB_NUM_SLAVES  %s\n"%self.VIP_DB['APB']['VipSlaveNum'])
        filename.write("\n")
        filename.write("class apb_cust_config extends uvm_object;\n")
        filename.write("\n")
        # filename.write("    svt_apb_system_configuration    apb_cfg;\n")
        # if(self.VIP_DB['APB']['VipMasterNum']!=0):
        #     filename.write("    svt_apb_system_configuration    master_cfg;\n")
        # if(self.VIP_DB['APB']['VipSlaveNum']!=0):
        #     filename.write("    svt_apb_system_configuration    slave_cfg;\n")
        for i in range(self.VIP_DB['APB']['VipMasterNum']):
            filename.write("    svt_apb_system_configuration    master%s_cfg;\n"%i)
        for i in range(self.VIP_DB['APB']['VipSlaveNum']):
            filename.write("    svt_apb_system_configuration    slave%s_cfg;\n"%i)

        filename.write("\n")
        filename.write("    `uvm_object_utils_begin(apb_cust_config)\n")
        # if(self.VIP_DB['APB']['VipMasterNum']!=0):
        #     filename.write("        `uvm_field_object(master_cfg,UVM_DEFAULT)\n")
        # if(self.VIP_DB['APB']['VipSlaveNum']!=0):
        #         filename.write("        `uvm_field_object(slave_cfg,UVM_DEFAULT)\n")
        for i in range(self.VIP_DB['APB']['VipMasterNum']):
            filename.write("        `uvm_field_object(master%s_cfg,UVM_DEFAULT)\n"%i)
        for i in range(self.VIP_DB['APB']['VipSlaveNum']):
            filename.write("        `uvm_field_object(slave%s_cfg,UVM_DEFAULT)\n"%i)

        filename.write("    `uvm_object_utils_end\n")
        filename.write("\n")
        filename.write("    function new(string name=\"apb_cust_config\");\n")
        filename.write("        super.new(name);\n")
        filename.write("\n")
        # filename.write("        apb_cfg=new(\"apb_cfg\");\n")
        # filename.write("\n")
        # filename.write("        apb_cfg.num_masters=`PRJ_APB_NUM_MASTERS;\n")
        # filename.write("        apb_cfg.num_slaves =`PRJ_APB_NUM_SLAVES;\n")
        # if(self.VIP_DB['APB']['VipMasterNum']!=0):
        #     filename.write("        master_cfg=new(\"master_cfg\");\n")
        # if(self.VIP_DB['APB']['VipSlaveNum']!=0):
        #     filename.write("        slave_cfg=new(\"slave_cfg\");\n")
        for i in range(self.VIP_DB['APB']['VipMasterNum']):
            filename.write("        master%s_cfg=new(\"master%s_cfg\");\n"%(i,i))
        for i in range(self.VIP_DB['APB']['VipSlaveNum']):
            filename.write("        slave%s_cfg=new(\"slave%s_cfg\");\n"%(i,i))

        filename.write("\n")
        filename.write("        //Create master port configurations\n")
        for i in range(self.VIP_DB['APB']['VipMasterNum']):
            MasterID="Master%s"%i
            filename.write("        master%s_cfg.paddr_width=svt_apb_system_configuration::PADDR_WIDTH_%s;\n"%(i,self.VIP_DB_Feature['APB'][MasterID]['AddrWidth']))
            filename.write("        master%s_cfg.pdata_width=svt_apb_system_configuration::PDATA_WIDTH_%s;\n"%(i,self.VIP_DB_Feature['APB'][MasterID]['DataWidth']))
            filename.write("        master%s_cfg.num_slaves                       =0;\n"    %i)
            filename.write("        master%s_cfg.is_active                        =1;\n"    %i)
            filename.write("        master%s_cfg.apb3_enable                      =0;\n"    %i)
            filename.write("        master%s_cfg.apb4_enable                      =1;\n"    %i)
            filename.write("        master%s_cfg.wait_for_reset_enable            =1;\n"    %i)
            filename.write("        master%s_cfg.disable_x_check_of_presetn       =1;\n"    %i)
            filename.write("        master%s_cfg.disable_x_check_of_pclk          =1;\n"    %i)
            filename.write("        master%s_cfg.transaction_coverage_enable      =0;\n"    %i)
            filename.write("        master%s_cfg.protocol_checks_coverage_enable  =1;\n"    %i)
            filename.write("        master%s_cfg.enable_complex_memory_map        =0;\n"    %i)
            filename.write("\n")

        filename.write("\n")
        filename.write("        //Create slave port configurations\n")
        for i in range(self.VIP_DB['APB']['VipSlaveNum']):
            SlaveID="Slave%s"%i
            filename.write("        slave%s_cfg.paddr_width=svt_apb_system_configuration::PADDR_WIDTH_%s;\n"%(i,self.VIP_DB_Feature['APB'][SlaveID]['AddrWidth']))
            filename.write("        slave%s_cfg.pdata_width=svt_apb_system_configuration::PDATA_WIDTH_%s;\n"%(i,self.VIP_DB_Feature['APB'][SlaveID]['DataWidth']))
            filename.write("        slave%s_cfg.num_slaves                       =1;\n"    %i)
            filename.write("        slave%s_cfg.is_active                        =0;\n"    %i)
            filename.write("        slave%s_cfg.apb3_enable                      =0;\n"    %i)
            filename.write("        slave%s_cfg.apb4_enable                      =1;\n"    %i)
            filename.write("        slave%s_cfg.wait_for_reset_enable            =1;\n"    %i)
            filename.write("        slave%s_cfg.disable_x_check_of_presetn       =1;\n"    %i)
            filename.write("        slave%s_cfg.disable_x_check_of_pclk          =1;\n"    %i)
            filename.write("        slave%s_cfg.transaction_coverage_enable      =0;\n"    %i)
            filename.write("        slave%s_cfg.protocol_checks_coverage_enable  =1;\n"    %i)
            filename.write("        slave%s_cfg.enable_complex_memory_map        =0;\n"    %i)
            filename.write("\n")

        filename.write("    endfunction\n")
        filename.write("\n")
        filename.write("endclass\n")
        filename.write("\n")
        filename.write("`endif\n")
        filename.close()
        #############################apb_sequence_lib.sv########################################################
        filename = open("apb_sequence_lib.sv", "w+")
        filename.write("`ifndef _APB_SEQUENCE_LIB_SV\n")
        filename.write("`define _APB_SEQUENCE_LIB_SV\n")
        filename.write("\n")
        # # apb_base_seq
        # filename.write("class apb_base_seq extends svt_apb_system_base_sequence;\n")
        # filename.write("\n")
        # filename.write("    apb_cust_config   apb_cfg;\n")
        # filename.write("\n")
        # filename.write("    `uvm_object_utils_begin(apb_base_seq)\n")
        # filename.write("        `uvm_field_object(apb_cfg,UVM_DEFAULT)\n")
        # filename.write("    `uvm_object_utils_end\n")
        # filename.write("\n")
        # filename.write("    function new(string name=\"apb_base_seq\");\n")
        # filename.write("        super.new(name);\n")
        # filename.write("    endfunction\n")
        # filename.write("\n")
        # filename.write("    virtual task pre_start();\n")
        # filename.write("        //`uvm_info(get_full_name(),\"pre_start\",UVM_LOW)\n")
        # filename.write("        if(starting_phase!=null)\n")
        # filename.write("            starting_phase.raise_objection(this);\n")
        # filename.write("    endtask\n")
        # filename.write("\n")
        # filename.write("    virtual task post_start();\n")
        # filename.write("        //`uvm_info(get_full_name(),\"post_start\",UVM_LOW)\n")
        # filename.write("        if(starting_phase!=null)\n")
        # filename.write("            starting_phase.raise_objection(this);\n")
        # filename.write("    endtask\n")
        # filename.write("\n")
        # filename.write("    virtual task body();\n")
        # filename.write("        //`uvm_info(get_full_name(),\"body\",UVM_LOW)\n")
        # filename.write("    endtask\n")
        # filename.write("\n")
        # filename.write("endclass:apb_base_seq\n")
        # filename.write("\n")

        # apb_master_wr_directed_seq
        filename.write("class apb_master_wr_directed_seq extends svt_apb_master_base_sequence;\n")
        filename.write("\n")
        filename.write("    rand bit[15:0]write_addr;\n")
        filename.write("    rand bit[31:0]write_data;\n")
        filename.write("\n")
        filename.write("    `uvm_object_utils(apb_master_wr_directed_seq)\n")
        filename.write("\n")
        filename.write("    function new(string name=\"apb_master_wr_directed_seq\");\n")
        filename.write("        super.new(name);\n")
        filename.write("    endfunction\n")
        filename.write("\n")
        filename.write("    virtual task body();\n")
        filename.write("        //`uvm_info(get_full_name(),\"body\",UVM_LOW)\n")
        filename.write("        svt_apb_master_transaction  write_tran;\n")
        filename.write("        svt_configuration           get_cfg;\n")
        filename.write("        super.body();\n")
        filename.write("        `uvm_info(get_full_name(),\"apb sequence body Write Entered ...\",UVM_LOW)\n")
        filename.write("        //p_sequencer.get(get_cfg);\n")
        filename.write("        //if(!cast(cfg,get_cfg))begin\n")
        filename.write("        //    `uvm_fatal(\"get_full_name\",\"Unable to cast the configuration to a svt_apb_system_configuration class\")\n")
        filename.write("        //end\n")
        filename.write("        `uvm_create(write_tran)\n")
        filename.write("        write_tran.cfg              =cfg;\n")
        filename.write("        write_tran.xact_type        =svt_apb_transaction::WRITE;\n")
        filename.write("        write_tran.address          =write_addr;\n")
        filename.write("        write_tran.data             =write_data;\n")
        filename.write("        write_tran.pstrb            ='hF;\n")
        filename.write("        write_tran.pprot0           =svt_apb_transaction::NORMAL;\n")
        filename.write("        write_tran.pslverr_enable   =1;\n")
        filename.write("        write_tran.num_idle_cycles  =1;\n")
        filename.write("        write_tran.num_wait_cycles  =1;\n")
        filename.write("        `uvm_info(get_full_name(),$sformatf(\"write data=%h\",write_data),UVM_LOW)\n")
        filename.write("        `uvm_send(write_tran)\n")
        filename.write("        get_response(rsp);\n")
        filename.write("        `uvm_info(get_full_name(),\"apb sequence body Write Exiting ...\",UVM_LOW)\n")
        filename.write("    endtask\n")
        filename.write("\n")
        filename.write("endclass:apb_master_wr_directed_seq\n")
        filename.write("\n")
        # apb_master_rd_directed_seq
        filename.write("class apb_master_rd_directed_seq extends svt_apb_master_base_sequence;\n")
        filename.write("\n")
        filename.write("    rand bit[15:0]read_addr;\n")
        filename.write("    rand bit[31:0]read_data;\n")
        filename.write("\n")
        filename.write("    `uvm_object_utils(apb_master_rd_directed_seq)\n")
        filename.write("\n")
        filename.write("    function new(string name=\"apb_master_rd_directed_seq\");\n")
        filename.write("        super.new(name);\n")
        filename.write("    endfunction\n")
        filename.write("\n")
        filename.write("    virtual task body();\n")
        filename.write("        //`uvm_info(get_full_name(),\"body\",UVM_LOW)\n")
        filename.write("        svt_apb_master_transaction  read_tran;\n")
        filename.write("        svt_configuration           get_cfg;\n")
        filename.write("        super.body();\n")
        filename.write("        `uvm_info(get_full_name(),\"apb sequence body Read Entered ...\",UVM_LOW)\n")
        filename.write("        //p_sequencer.get_cfg(get_cfg);\n")
        filename.write("        //if(!cast(cfg,get_cfg))begin\n")
        filename.write("        //    `uvm_fatal(\"body\",\"Unable to $cast the configuration to a svt_apb_port_configuration class\");\n")
        filename.write("        //end\n")
        filename.write("        `uvm_create(read_tran)\n")
        filename.write("        read_tran.cfg              =cfg;\n")
        filename.write("        read_tran.xact_type        =svt_apb_transaction::READ;\n")
        filename.write("        read_tran.address          =read_addr;\n")
        filename.write("        `uvm_send(read_tran)\n")
        filename.write("        get_response(rsp);\n")
        filename.write("        read_data            =rsp.data;\n")
        filename.write("        `uvm_info(get_full_name(),$sformatf(\"read data=%h\",read_data),UVM_LOW)\n")
        filename.write("        `uvm_info(get_full_name(),\"apb sequence body Read Exiting ...\",UVM_LOW)\n")
        filename.write("    endtask\n")
        filename.write("\n")
        filename.write("endclass:apb_master_rd_directed_seq\n")
        filename.write("\n")
        filename.write("`endif\n")
        filename.close()
        # apb_slave_memory_seq

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")
 
            
if __name__ == '__main__':
    gen=gen_apb_uvc()