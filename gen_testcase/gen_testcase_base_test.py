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

class gen_testcase_base_test:

    def __init__(self):
        print("[gen_testcase_base_test]:initial")
        #EnvironmentGenCfg='../VerifyEnvironmentGenCfg.xlsx'
        EnvironmentGenCfg=Parameters.EnvironmentGenCfg
        readexcel_WorkingDirectoryGen.readexcel_WorkingDirectoryGen_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_VIP.readexcel_VIP_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_ClockRst.readexcel_ClockRst_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_DutSignal.readexcel_DutSignal_info(self,EnvironmentGenCfg,PrintEnable=False)
        self.gen_testcase_base_test_info(self.tb_name,self.DUT_GroupName,PrintEnable=True)

    def gen_testcase_base_test_info(self,name,DUT_GroupName,PrintEnable):
        filename = open("%s_base_test.sv"%name, "w+",encoding="utf-8")
        filename.write("`ifndef _%s_BASE_TEST_SV_\n"%name.upper())
        filename.write("`define _%s_BASE_TEST_SV_\n"%name.upper())
        filename.write("\n")
        filename.write("//uvm hdl task,获取后门的访问rtl的办法\n")
        filename.write("//1.int uvm_hdl_check_path(string path)   path指定的信号，是否存在 返回值\n")
        filename.write("//2.int uvm_hdl_deposit(string path, uvm_hdl_data_t value) 将path指定的信号，设置为value值  返回值\n")
        filename.write("//3.int uvm_hdl_force(string path, uvm_hdl_data_t value) 将path指定的信号，force成value值 返回值\n")
        filename.write("//4.int uvm_hdl_release(string path) 将path指定的信号，release 返回值\n")
        filename.write("//5.int uvm_hdl_read(string path,  output uvm_hdl_data_t value) 读取path指定的信号值，保存在value中 返回值\n")
        filename.write("//6.int uvm_hdl_release_and_read(string path, inout uvm_hdl_data_t value)\n")
        filename.write("\n")
        filename.write("class %s_base_test extends uvm_test;\n"%name)
        filename.write("\n")
        filename.write("\t/*Import the output information into a file*/\n")
        filename.write("\t// UVM_FILE    info_log;\n")
        filename.write("\t// UVM_FILE    warning_log;\n")
        filename.write("\t// UVM_FILE    error_log;\n")
        filename.write("\t// UVM_FILE    fatal_log;\n")
        filename.write("\n")
        filename.write("\t//uvm_cmdline_process UCP\n")
        filename.write("\tvirtual %s_vif    %svif;\n"%(name,name))
        filename.write("\n")
        filename.write("\t%s_env            env;\n"%name)
        filename.write("\n")
        filename.write("\t%s_config         %s_cfg;\n"%(name,name))
        filename.write("\t%s_event          %s_evt;\n"%(name,name))
        filename.write("\n")
        for i in range(len(DUT_GroupName)):
            # #[not vip]:
            # if self.DUT_VIP[i]==False:
            #     filename.write("\t%s_config            %s_cfg;\n"%(DUT_GroupName[i],DUT_GroupName[i]))
            if self.DUT_VIP[i]==True:filename.write("\t`ifndef NO_%s_CUSTOM\n"%self.DUT_GroupName[i])
            filename.write("\t%s_config            %s_cfg;\n"%(DUT_GroupName[i],DUT_GroupName[i]))
            if self.DUT_VIP[i]==True:filename.write("\t`endif\n")
        filename.write("\n")
        filename.write("\t`ifdef REG_MODEL;\n")
        filename.write("\t\t%s_reg_top  RegModel;\n"%name)
        filename.write("\t`endif\n")
        filename.write("\n")
        #if self.vip_axi_enable:
        if self.VIP_DB['AXI']['Enable']:
            filename.write("\taxi_cust_config     axi_cfg;\n")
            #or i in range(0,self.VIP_axi_slave_num):
            for i in range(self.VIP_DB['AXI']['VipSlaveNum']):
                filename.write("\taxi_slave_mem_response_sequence     axi_slave_seq%s;\n"%i)

        filename.write("\n")
        filename.write("\t`uvm_component_utils(%s_base_test)\n"%name)
        filename.write("\n")

        # filename.write("\tfunction new(string name=\"%s_base_test\",uvm_component parent=null);\n")
        # filename.write("\t\tsuper.new(name,parent);\n")
        # filename.write("\t\t%s_cfg=%s_config::type_id::create(\"%s_cfg\",this);\n"%(name,name,name))
        # filename.write("\t\t%s_evt=%s_event::type_id::create(\"%s_evt\",this);\n"%(name,name,name))
        # filename.write("\n")
        # #if self.vip_axi_enable:
        # if self.VIP_DB['AXI']['Enable']:
        #     filename.write("\t\taxi_cfg=axi_cust_config::type_id::create(\"axi_cfg\",this);\n")
        #     filename.write("\n")
        #     #for i in range(0,self.VIP_axi_slave_num):
        #     for i in range(self.VIP_DB['AXI']['VipSlaveNum']):
        #         filename.write("\t\taxi_slave_seq%s=new(\"axi_slave_seq%s\");\n"%(i,i))
        #     filename.write("\n")
        # filename.write("\t\tenv=%s_env::type_id::create(\"env\",this);\n"%name)
        # filename.write("\n")
        # filename.write("\t\t`ifdef REG_MODEL;\n")
        # filename.write("\t\t\tRegModel=env.RegModel;\n")
        # filename.write("\t\t`endif\n")
        # filename.write("\n")
        # filename.write("\t\t//UCP=uvm_cmdline_processor::get_inst();\n")
        # filename.write("\t\t//UCP.get_arg_value(\"+UVM_TESTNAME\",%svif.TestCaseName);\n"%name)
        # filename.write("\n")
        # filename.write("\tendfunction\n")
        # filename.write("\n")

        StrStr=[]
        StrStr.append("%s_cfg=%s_config::type_id::create(\"%s_cfg\",this);"%(name,name,name))
        StrStr.append("%s_evt=%s_event::type_id::create(\"%s_evt\",this);"%(name,name,name))
        for i in range(len(DUT_GroupName)):
            # #[not vip]:
            # if self.DUT_VIP[i]==False:
            #     StrStr.append("%s_cfg=%s_config::type_id::create(\"%s_cfg\",this);"
            #                   %(DUT_GroupName[i],DUT_GroupName[i],DUT_GroupName[i]))
            if self.DUT_VIP[i]==True:StrStr.append("`ifndef NO_%s_CUSTOM"%self.DUT_GroupName[i])
            StrStr.append("%s_cfg=%s_config::type_id::create(\"%s_cfg\",this);"%(DUT_GroupName[i],DUT_GroupName[i],DUT_GroupName[i]))
            if self.DUT_VIP[i]==True:StrStr.append("`endif")
        
        # if self.VIP_DB['APB']['Enable']:
        #     StrStr.append("apb_cfg=apb_cust_config::type_id::create(\"apb_cfg\",this);")
        
        # if self.VIP_DB['AHB']['Enable']:
        #     StrStr.append("ahb_cfg=ahb_cust_config::type_id::create(\"ahb_cfg\",this);")

        #if self.vip_axi_enable:
        if self.VIP_DB['AXI']['Enable']:
            StrStr.append("axi_cfg=axi_cust_config::type_id::create(\"axi_cfg\",this);")
            #for i in range(0,self.VIP_axi_slave_num):
            for i in range(self.VIP_DB['AXI']['VipSlaveNum']):
                StrStr.append("axi_slave_seq%s=new(\"axi_slave_seq%s\");"%(i,i))

        StrStr.append("")
        StrStr.append("env=%s_env::type_id::create(\"env\",this);"%name)
        StrStr.append("`ifdef REG_MODEL;")
        StrStr.append("\tRegModel=env.RegModel;")
        StrStr.append("`endif")
        StrStr.append("//UCP=uvm_cmdline_processor::get_inst();")
        StrStr.append("//UCP.get_arg_value(\"+UVM_TESTNAME\",%svif.TestCaseName);"%name)
        gen_uvm_new(self,filename,'%s_base_test'%name,'uvm_component',StrStr,Parameters.PrintEnable)

        # #build_phase
        # filename.write("\tvirtual function void build_phase(uvm_phase phase);\n")
        # filename.write("\t\tsuper.build_phase(phase);\n")
        # filename.write("\n")
        # filename.write("\t\tuvm_config_db#(%s_config)::set(this,\"*\",\"%s_cfg\",%s_cfg)\n"%(name,name,name))
        # #if self.vip_axi_enable:
        # if self.VIP_DB['AXI']['Enable']:
        #     filename.write("\t\tuvm_config_db#(svt_axi_system_configuration)::set(this,\"env.axi_system_env\",\"axi_cfg\",axi_cfg.axi_cfg)\n")
        #     #for i in range(0,self.VIP_axi_slave_num):
        #     for i in range(self.VIP_DB['AXI']['VipSlaveNum']):
        #         filename.write("\t\taxi_cfg.axi_cfg.set_addr_range(%s,64'h0000,64'hFFFF);\n"%i)
        # filename.write("\n")
        # filename.write("\t\tif(!uvm_config_db#(%s_vif)::get(this,"",\"%s_vif\",%svif))\n"%(name,name,name))
        # filename.write("\t\t\t`uvm_fatal(\"%s_vif\",\"virtual interface must be set for it!!!\");\n"%name)
        # filename.write("\n")
        # filename.write("\tendfunction\n")
        # filename.write("\n")

        StrStr=[]
        StrStr.append("uvm_config_db#(%s_config)::set(this,\"*\",\"%s_config\",%s_cfg);"%(name,name,name))
        for i in range(len(DUT_GroupName)):
            # #[not vip]:
            # if self.DUT_VIP[i]==False:
            #     StrStr.append("uvm_config_db#(%s_config)::set(this,\"*\",\"%s_config\",%s_cfg);"
            #                   %(DUT_GroupName[i],DUT_GroupName[i],DUT_GroupName[i]))
            if self.DUT_VIP[i]==True:StrStr.append("`ifndef NO_%s_CUSTOM"%self.DUT_GroupName[i])
            StrStr.append("uvm_config_db#(%s_config)::set(this,\"*\",\"%s_config\",%s_cfg);"%(DUT_GroupName[i],DUT_GroupName[i],DUT_GroupName[i]))
            if self.DUT_VIP[i]==True:StrStr.append("`endif")

        # if self.VIP_DB['APB']['Enable']:
        #     StrStr.append("uvm_config_db#(svt_apb_system_configuration)::set(this,\"env.apb_system_env\",\"apb_cfg\",apb_cfg.apb_cfg)")

        # if self.VIP_DB['APB']['Enable']:
        #     StrStr.append("uvm_config_db#(svt_ahb_system_configuration)::set(this,\"env.ahb_system_env\",\"ahb_cfg\",ahb_cfg.ahb_cfg)")
            
        #if self.vip_axi_enable:
        if self.VIP_DB['AXI']['Enable']:
            StrStr.append("uvm_config_db#(svt_axi_system_configuration)::set(this,\"env.axi_system_env\",\"axi_cfg\",axi_cfg.axi_cfg)")
            #for i in range(0,self.VIP_axi_slave_num):
            for i in range(self.VIP_DB['AXI']['VipSlaveNum']):
                StrStr.append("axi_cfg.axi_cfg.set_addr_range(%s,64'h0000,64'hFFFF);"%i)

        StrStr.append("")        
        StrStr.append("if(!uvm_config_db#(virtual %s_vif)::get(this,\"\",\"%s_vif\",%svif))"%(name,name,name))
        StrStr.append("\t`uvm_fatal(\"%s_vif\",\"virtual interface must be set for it!!!\");"%name)
        gen_uvm_phase(self,filename,'build_phase'               ,StrStr,Parameters.PrintEnable)

        StrStr.append("")
        StrStr.append("/*Set the print redundancy threshold*/")
        StrStr.append("/*typedef enum{UVM_NONE=0,UVM_LOW=100,UVM_MEDIUM=200,UVM_HIGH=300,UVM_FULL=400,UVM_DEBUG=500} uvm_verbosity;*/")
        StrStr.append("//   $display(\"env.i_agt.drv.get_report_verbosity_level=%0d\",env.i_agt.drv.get_report_verbosity_level());")
        StrStr.append("//   env.i_agt.drv.set_report_verbosity_level(UVM_HIGH);")
        StrStr.append("//   env.i_agt.set_report_verbosity_level_hier(UVM_HIGH);")
        StrStr.append("//   env.i_agt.drv.set_report_id_verbosity(\"ID\",UVM_HIGH);")
        StrStr.append("//   env.i_agt.set_report_id_verbosity_hier(\"ID\",UVM_HIGH);")
        StrStr.append("/*The command line implements Set the print redundancy threshold*/")
        StrStr.append("//   +UVM_VERBOSITY=UVM_HIGH")
        StrStr.append("")
        StrStr.append("/*Overload the severity of the printed information(WARNING->ERROR)*/")
        StrStr.append("//   env.i_agt.drv.set_report_severity_override(UVM_WARNING,UVM_ERROR);")
        StrStr.append("//   env.i_agt.drv.set_report_severity_override(UVM_WARNING,\"ID\",UVM_ERROR);")
        StrStr.append("/*The command line implements the severity of overloading print information*/")
        StrStr.append("/*Command line format: +uvm_set_severity=<component>,<id>,<old severity>,<new severity>*/")
        StrStr.append("//   +uvm_set_severity=\"uvm_test_top.env.i_agt.drv,ID,UVM_WARNING,UVM_ERROR\"")
        StrStr.append("//   +uvm_set_severity=\"uvm_test_top.env.i_agt.drv,_ALL_,UVM_WARNING,UVM_ERROR\"")
        StrStr.append("")
        StrStr.append("/*The simulation ends when the number of UVM_ERROR reaches a certain threshold*/")
        StrStr.append("//   set_report_max_quit_count(5);")
        StrStr.append("/*The command line implements The simulation ends when the number of UVM_ERROR reaches a certain threshold*/")
        StrStr.append("//   +UVM_MAX_QUIT_COUNT=6,NO/YES")
        StrStr.append("")
        StrStr.append("/*Control the behavior of printing information*/")
        StrStr.append("/*typedef enum{UVM_NO_ACTION=0,UVM_DISPLAY=1,UVM_LOG=2,UVM_COUNT=4,UVM_EXIT=8,UVM_CALL_HOOK=16,UVM_STOP=32} uvm_action_type;*/")
        StrStr.append("")
        StrStr.append("/*Import the output information into a file*/")
        StrStr.append("//   info/waning/error/fatal_log=$fopen(\"info/waning/error/fatal.log\",\"w\")")
        StrStr.append("//   env.i_agt.drv.set_report_severity_file(UVM_INFO/WARNING/ERROR/FATAL,info/waning/error/fatal_log);")
        StrStr.append("//   env.i_agt.set_report_severity_file_hier(UVM_INFO/WARNING/ERROR/FATAL,info/waning/error/fatal_log);")
        StrStr.append("//   env.i_agt.drv.set_report_severity_action(UVM_INFO       ,UVM_DISPLAY | UVM_LOG);")
        StrStr.append("//   env.i_agt.drv.set_report_severity_action(UVM_WARNING    ,UVM_DISPLAY | UVM_LOG);")
        StrStr.append("//   env.i_agt.drv.set_report_severity_action(UVM_ERROR      ,UVM_DISPLAY | UVM_COUNT | UVM_LOG);")
        StrStr.append("//   env.i_agt.drv.set_report_severity_action(UVM_FATAL      ,UVM_DISPLAY | UVM_EXIT  | UVM_LOG);")
        StrStr.append("")
        StrStr.append("")
        gen_uvm_phase(self,filename,'connect_phase'             ,StrStr,Parameters.PrintEnable)

        StrStr=[]
        StrStr.append("//uvm_top.print_topology();")
        gen_uvm_phase(self,filename,'end_of_elaboration_phase'  ,StrStr,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'start_of_simulation_phase' ,None,Parameters.PrintEnable)

        StrStr=[]
        StrStr.append("phase.raise_objection(this);")
        StrStr.append("//@(posedge %svif.rstn);"%name)
        StrStr.append("//#1us;")
        StrStr.append("phase.drop_objection(this);")
        gen_uvm_phase(self,filename,'run_phase'                 ,StrStr,Parameters.PrintEnable)

        StrStr=[]
        StrStr.append("//phase.phase_done.set_drain_time(this,4000);")
        gen_uvm_phase(self,filename,'main_phase'                 ,StrStr,Parameters.PrintEnable)

        gen_uvm_phase(self,filename,'extract_phase'             ,None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'check_phase'               ,None,Parameters.PrintEnable)

        # StrStr=[]
        # StrStr.append("uvm_report_server    server;")
        # StrStr.append("int                  err_num;")
        # StrStr.append("")
        # StrStr.append("server   =get_report_server();")
        # StrStr.append("err_num  =server.get_severity_count(UVM_ERROR);")
        # StrStr.append("")
        # StrStr.append("if(err_num==0)")
        # StrStr.append("    `uvm_info(get_type_name(),\"===UVM TEST PASSED===\",UVM_LOW)")
        # StrStr.append("else")
        # StrStr.append("    `uvm_info(get_type_name(),\"===UVM TEST FAILED===\",UVM_LOW)")
        # gen_uvm_phase(self,filename,'report_phase'              ,StrStr,Parameters.PrintEnable)

        filename.write("\n")
        filename.write("    //report_phase\n")
        filename.write("    virtual function void report_phase(uvm_phase phase);\n")
        filename.write("        //super.report_phase(phase);\n")
        filename.write("        uvm_report_server    server;\n")
        filename.write("        int                  err_num;\n")
        filename.write("\n")
        filename.write("        server   =get_report_server();\n")
        filename.write("        err_num  =server.get_severity_count(UVM_ERROR);\n")
        filename.write("\n")
        filename.write("        if(err_num==0)\n")
        filename.write("            if(get_report_verbosity_level()==0)\n")
        filename.write("                $display(\"===UVM TEST PASSED===\");\n")
        filename.write("            else\n")
        filename.write("                `uvm_info(get_type_name(),\"===UVM TEST PASSED===\",UVM_LOW)\n")
        filename.write("        else\n")
        filename.write("            if(get_report_verbosity_level()==0)\n")
        filename.write("                $display(\"===UVM TEST FAILED===\");\n")
        filename.write("            else\n")
        filename.write("                `uvm_info(get_type_name(),\"===UVM TEST FAILED===\",UVM_LOW)\n")
        filename.write("    endfunction\n")
        filename.write("\n")

        gen_uvm_phase(self,filename,'final_phase'               ,None,Parameters.PrintEnable)

        # #connect_phase
        # filename.write("\tvirtual function void connect_phase(uvm_phase phase);\n")
        # filename.write("\t\tsuper.connect_phase(phase);\n")
        # filename.write("\tendfunction\n")
        # filename.write("\n")
        # #[phase]:end_of_elaboration_phase
        # filename.write("\tvirtual function void end_of_elaboration_phase(uvm_phase phase);\n")
        # filename.write("\t\tsuper.end_of_elaboration_phase(phase);\n")
        # filename.write("\tendfunction\n")
        # filename.write("\n")
        # #[phase]:start_of_simulation_phase
        # filename.write("\tvirtual function void start_of_simulation_phase(uvm_phase phase);\n")
        # filename.write("\t\tsuper.start_of_simulation_phase(phase);\n")
        # filename.write("\tendfunction\n")
        # filename.write("\n")
        # #[phase]:main_phase
        # filename.write("\t//run_phase\n")
        # filename.write("\t//<pre_/post_/reset_phase><pre_/post_/configure_phase><pre_/post_/main_phase><pre_/post_/shutdown_phase>\n")
        # filename.write("\ttask run_phase(uvm_phase phase);\n")
        # filename.write("\t\tsuper.run_phase(phase)\n")
        # filename.write("\tendtask\n")
        # filename.write("\n")
        # #[phase]:extract_phase
        # filename.write("\tvirtual function void extract_phase(uvm_phase phase);\n")
        # filename.write("\t\tsuper.extract_phase(phase);\n")
        # filename.write("\tendfunction\n")
        # filename.write("\n")
        # #[phase]:check_phase
        # filename.write("\tvirtual function void check_phase(uvm_phase phase);\n")
        # filename.write("\t\tsuper.check_phase(phase);\n")
        # filename.write("\tendfunction\n")
        # filename.write("\n")
        # #[phase]:report_phase
        # filename.write("\tvirtual function void report_phase(uvm_phase phase);\n")
        # filename.write("\t\tsuper.report_phase(phase);\n")
        # filename.write("\tendfunction\n")
        # filename.write("\n")
        # #[phase]:final_phase
        # filename.write("\tvirtual function void final_phase(uvm_phase phase);\n")
        # filename.write("\t\tsuper.final_phase(phase);\n")
        # filename.write("\tendfunction\n")
        # filename.write("\n")

        filename.write("endclass\n")
        filename.write("\n")
        filename.write("`endif\n")
        filename.close()

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")
            
if __name__ == '__main__':
    gen=gen_testcase_base_test()