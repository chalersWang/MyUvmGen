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

class gen_env_env:

    def __init__(self):
        print("[gen_env_EnvTop]:initial")
        #EnvironmentGenCfg='../VerifyEnvironmentGenCfg.xlsx'
        EnvironmentGenCfg=Parameters.EnvironmentGenCfg
        readexcel_WorkingDirectoryGen.readexcel_WorkingDirectoryGen_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_VIP.readexcel_VIP_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_ClockRst.readexcel_ClockRst_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_DutSignal.readexcel_DutSignal_info(self,EnvironmentGenCfg,PrintEnable=False)
        self.gen_env_env_info(PrintEnable=True)

    def gen_env_env_info(self,PrintEnable):
        filename = open("%s_env.sv"%self.tb_name, "w+")
        filename.write("`ifndef _%s_ENV_SV_\n" %self.tb_name.upper())
        filename.write("`define _%s_ENV_SV_\n" %self.tb_name.upper())
        filename.write("\n")
        filename.write("class %s_env extends uvm_env;\n" %self.tb_name)
        filename.write("\n")
        
        #env cfg/event/virtual/scb
        filename.write("\t%s_config             %s_cfg;\n"%(self.tb_name,self.tb_name))
        filename.write("\t%s_event              %s_evt;\n"%(self.tb_name,self.tb_name))
        filename.write("\t%s_virtual_sequencer  %s_vseqr;\n"%(self.tb_name,self.tb_name))
        filename.write("\t%s_scoreboard         %s_scb;\n"%(self.tb_name,self.tb_name))
        filename.write("\n")
        # #apb
        # #if self.vip_apb_enable:
        # if self.VIP_DB['APB']['Enable']:
        #     filename.write("\tsvt_apb_system_env   apb_system_env;\n")
        #     filename.write("\tapb_cust_config      apb_cfg;\n")
        # filename.write("\n")
        # #ahb
        # #if self.vip_ahb_enable:
        # if self.VIP_DB['AHB']['Enable']:
        #     filename.write("\tsvt_ahb_system_env   ahb_system_env;\n")
        #     filename.write("\tahb_cust_config      ahb_cfg;\n")
        # filename.write("\n")
        # #axi
        # #if self.vip_axi_enable:
        # if self.VIP_DB['AXI']['Enable']:
        #     filename.write("\tsvt_axi_system_env   axi_system_env;\n")
        #     filename.write("\taxi_cust_config      axi_cfg;\n")
        # filename.write("\n")
        for VipName in self.VIP_DB.keys():
            if self.VIP_DB[VipName]['Enable']:
                # filename.write("\tsvt_%s_system_env   %s_system_env;\n" %(VipName.lower(),VipName.lower()))
                filename.write("\t`ifndef NO_%s_VIP\n"%VipName)
                # APB
                if(VipName=='APB'):
                    for i in range(self.VIP_DB['APB']['VipMasterNum']):
                        filename.write("\tsvt_apb_system_env   apb_system_master%s_env;\n" %i)
                    for i in range(self.VIP_DB['APB']['VipSlaveNum']):
                        filename.write("\tsvt_apb_system_env   apb_system_slave%s_env;\n" %i)
                # AHB
                if(VipName=='AHB'):
                    filename.write("\tsvt_ahb_system_env   ahb_system_env;\n") 
                # AXI
                if(VipName=='AXI'):
                    filename.write("\tsvt_axi_system_env   axi_system_env;\n")    
                filename.write("\t%s_cust_config      %s_cfg;\n"        %(VipName.lower(),VipName.lower()))
                filename.write("\t`endif\n")
                filename.write("\n")

        #uvc agent
        for i in range(len(self.DUT_GroupName)):
            if self.DUT_VIP[i]==False:
                filename.write("\t%s_agent    %s_agt;\n"%(self.DUT_GroupName[i],self.DUT_GroupName[i]))
            else:
                filename.write("\t`ifndef NO_%s_CUSTOM\n"%self.DUT_GroupName[i])
                filename.write("\t  %s_agent    %s_agt;\n"%(self.DUT_GroupName[i],self.DUT_GroupName[i]))
                filename.write("\t`endif\n")
        filename.write("\n")
        #reg model
        filename.write("\t`ifdef REG_MODEL\n")
        filename.write("\t\tstring      hdl_path;\n")
        filename.write("\t\t%s_reg_top  RegModel;\n"%self.tb_name)
        filename.write("\t`endif\n")
        filename.write("\n")
        filename.write("\t`uvm_component_utils(%s_env);\n"%self.tb_name)
        filename.write("\n")

        # filename.write("\tfunction new(string name=\"%s_env\",uvm_component parent=null);\n"%self.tb_name)
        # filename.write("\t\tsuper.new(name,parent);\n")
        # filename.write("\tendfunction\n")
        # filename.write("\n")

        # StrStr=[]
        # for VipName in self.VIP_DB.keys():
        #     if self.VIP_DB[VipName]['Enable']:
        #         vipname=VipName.lower()
        #         StrStr.append("`ifndef NO_%s_VIP"%VipName)
        #         StrStr.append("%s_cfg=%s_cust_config::type_id::create(\"%s_cfg\");"                                              %(vipname,vipname,vipname))
        #         # StrStr.append("uvm_config_db#(svt_%s_system_configuration)::set(this,\"%s_system_env\",\"cfg\",%s_cfg.%s_cfg);" %(vipname,vipname,vipname,vipname))   
        #         # StrStr.append("%s_system_env=svt_%s_system_env::type_id::create(\"%s_system_env\",this);"                       %(vipname,vipname,vipname)) 
        #         # APB
        #         if(VipName=='APB'):
        #             for i in range(self.VIP_DB['APB']['VipMasterNum']):
        #                 StrStr.append("uvm_config_db#(svt_apb_system_configuration)::set(this,\"apb_system_master%s_env\",\"cfg\",apb_cfg.master%s_cfg);"%(i,i))
        #                 # StrStr.append("uvm_config_db#(apb_cust_config)::set(this,\"apb_system_master%s_env\",\"cfg\",apb_cfg.master%s_cfg);"%(i,i))
        #                 StrStr.append("apb_system_master%s_env=svt_%s_system_env::type_id::create(\"apb_system_master%s_env\",this);"%(i,vipname,i))
        #             for i in range(self.VIP_DB['APB']['VipSlaveNum']):
        #                 StrStr.append("uvm_config_db#(svt_apb_system_configuration)::set(this,\"apb_system_slave%s_env\",\"cfg\",apb_cfg.slave%s_cfg);"%(i,i))
        #                 # StrStr.append("uvm_config_db#(apb_cust_config)::set(this,\"apb_system_slave%s_env\",\"cfg\",apb_cfg.slave%s_cfg);"%(i,i))
        #                 StrStr.append("apb_system_slave%s_env=svt_%s_system_env::type_id::create(\"apb_system_slave%s_env\",this);"%(i,vipname,i))
        #         # AHB
        #         if(VipName=='AHB'):
        #             StrStr.append("uvm_config_db#(svt_%s_system_configuration)::set(this,\"%s_system_env\",\"cfg\",%s_cfg.%s_cfg);" %(vipname,vipname,vipname,vipname)) 
        #             StrStr.append("%s_system_env=svt_%s_system_env::type_id::create(\"%s_system_env\",this);"                       %(vipname,vipname,vipname))
        #         # AXI
        #         if(VipName=='AXI'):
        #             StrStr.append("uvm_config_db#(svt_%s_system_configuration)::set(this,\"%s_system_env\",\"cfg\",%s_cfg.%s_cfg);" %(vipname,vipname,vipname,vipname))   
        #             StrStr.append("%s_system_env=svt_%s_system_env::type_id::create(\"%s_system_env\",this);"                       %(vipname,vipname,vipname))              
        #         StrStr.append("")
        #         StrStr.append("`endif")
        # #top
        # StrStr.append("%s_cfg    =%s_config::type_id::create(\"%s_cfg\",this);"                  %(self.tb_name,self.tb_name,self.tb_name))
        # StrStr.append("%s_evt    =%s_event::type_id::create(\"%s_evt\",this);"                   %(self.tb_name,self.tb_name,self.tb_name))
        # StrStr.append("%s_vseqr  =%s_virtual_sequencer::type_id::create(\"%s_vseqr\",this);"     %(self.tb_name,self.tb_name,self.tb_name))
        # StrStr.append("%s_scb    =%s_scoreboard::type_id::create(\"%s_scb\",this);"              %(self.tb_name,self.tb_name,self.tb_name))
        # StrStr.append("")
        # #uvc agent
        # for i in range(len(self.DUT_GroupName)):
        #     if self.DUT_VIP[i]==True:StrStr.append("`ifndef NO_%s_CUSTOM"%self.DUT_GroupName[i])
        #     StrStr.append("%s_agt =%s_agent::type_id::create(\"%s_agt\",this);"%(self.DUT_GroupName[i],self.DUT_GroupName[i],self.DUT_GroupName[i]))
        #     if self.DUT_VIP[i]==True:StrStr.append("`endif")
        # StrStr.append("")
        # for i in range(len(self.DUT_GroupName)):
        #     if self.DUT_VIP[i]==True:StrStr.append("`ifndef NO_%s_CUSTOM"%self.DUT_GroupName[i])
        #     StrStr.append("%s_agt.is_active=UVM_ACTIVE;"%self.DUT_GroupName[i])
        #     if self.DUT_VIP[i]==True:StrStr.append("`endif")
        # gen_uvm_new(self,filename,'%s_env'%self.tb_name,'uvm_component',StrStr,PrintEnable)
        gen_uvm_new(self,filename,'%s_env'%self.tb_name,'uvm_component',None,PrintEnable)

        # #[phase]:build_phase
        # filename.write("\tvirtual function void build_phase(uvm_phase phase);\n")
        # filename.write("\t\tsuper.build_phase(phase);\n")
        # filename.write("\n")
        # # #vip
        # # #if self.vip_apb_enable:
        # # if self.VIP_DB['APB']['Enable']:
        # #     filename.write("\t\tapb_cfg=apb_cust_config::type_id::create(\"apb_cfg\");\n")
        # #     filename.write("\t\tuvm_config_db#(svt_apb_system_configuration)::set(this,\"apb_system_env\",\"cfg\",apb_cfg.apb_cfg);\n")
        # #     filename.write("\t\tapb_system_env=svt_apb_system_env::type_id::create(\"apb_system_env\",this);\n")
        # # filename.write("\n")
        # # #if self.vip_ahb_enable:
        # # if self.VIP_DB['AHB']['Enable']:
        # #     filename.write("\t\tahb_cfg=ahb_cust_config::type_id::create(\"ahb_cfg\");\n")
        # #     filename.write("\t\tuvm_config_db#(svt_ahb_system_configuration)::set(this,\"ahb_system_env\",\"cfg\",ahb_cfg.ahb_cfg);\n")
        # #     filename.write("\t\tahb_system_env=svt_ahb_system_env::type_id::create(\"ahb_system_env\",this);\n")
        # # filename.write("\n")
        # # #if self.vip_axi_enable:
        # # if self.VIP_DB['AXI']['Enable']:
        # #     filename.write("\t\taxi_cfg=axi_cust_config::type_id::create(\"axi_cfg\");\n")
        # #     filename.write("\t\tuvm_config_db#(svt_axi_system_configuration)::set(this,\"axi_system_env\",\"cfg\",axi_cfg.axi_cfg);\n")
        # #     filename.write("\t\taxi_system_env=svt_axi_system_env::type_id::create(\"axi_system_env\",this);\n")
        # for VipName in self.VIP_DB.keys():
        #     if self.VIP_DB[VipName]['Enable']:
        #         vipname=VipName.lower()
        #         filename.write("\t\t%s_cfg=%s_cust_config::type_id::create(\"%s_cfg\");\n"                                              %(vipname,vipname,vipname))
        #         filename.write("\t\tuvm_config_db#(svt_%s_system_configuration)::set(this,\"%s_system_env\",\"cfg\",%s_cfg.%s_cfg);\n"  %(vipname,vipname,vipname,vipname))
        #         filename.write("\t\t%s_system_env=svt_%s_system_env::type_id::create(\"%s_system_env\",this);\n"                        %(vipname,vipname,vipname))
        #         filename.write("\n")

        # #top
        # filename.write("\t\t%s_cfg    =%s_config::type_id::create(\"%s_cfg\",this);\n"                  %(self.tb_name,self.tb_name,self.tb_name))
        # filename.write("\t\t%s_evt    =%s_event::type_id::create(\"%s_evt\",this);\n"                   %(self.tb_name,self.tb_name,self.tb_name))
        # filename.write("\t\t%s_vseqr  =%s_virtual_sequencer::type_id::create(\"%s_vseqr\",this);\n"     %(self.tb_name,self.tb_name,self.tb_name))
        # filename.write("\t\t%s_scb    =%s_scoreboard::type_id::create(\"%s_scb\",this);\n"              %(self.tb_name,self.tb_name,self.tb_name))
        # filename.write("\n")
        # #uvc agent
        # for i in range(len(self.DUT_GroupName)):
        #     if self.DUT_VIP[i]==False:
        #         filename.write("\t\t%s_agt =%s_agent::type_id::create(\"%s_agt\",this);\n"                  
        #                        %(self.DUT_GroupName[i],self.DUT_GroupName[i],self.DUT_GroupName[i]))
        # filename.write("\n")
        # filename.write("\t\tuvm_config_db#(%s_config)::set(null,\"\",\"%s_configuration\",%s_cfg);\n"   %(self.tb_name,self.tb_name,self.tb_name))
        # filename.write("\t\tuvm_config_db#(%s_event)::set(null,\"\",\"%s_event\",%s_evt);\n"            %(self.tb_name,self.tb_name,self.tb_name))
        # filename.write("\t\n")
        # filename.write("\tendfunction\n")
        # filename.write("\n")

        StrStr=[]
        for VipName in self.VIP_DB.keys():
            if self.VIP_DB[VipName]['Enable']:
                vipname=VipName.lower()
                StrStr.append("`ifndef NO_%s_VIP"%VipName)
                StrStr.append("%s_cfg=%s_cust_config::type_id::create(\"%s_cfg\");"                                              %(vipname,vipname,vipname))
                # StrStr.append("uvm_config_db#(svt_%s_system_configuration)::set(this,\"%s_system_env\",\"cfg\",%s_cfg.%s_cfg);" %(vipname,vipname,vipname,vipname))   
                # StrStr.append("%s_system_env=svt_%s_system_env::type_id::create(\"%s_system_env\",this);"                       %(vipname,vipname,vipname)) 
                # APB
                if(VipName=='APB'):
                    for i in range(self.VIP_DB['APB']['VipMasterNum']):
                        StrStr.append("uvm_config_db#(svt_apb_system_configuration)::set(this,\"apb_system_master%s_env\",\"cfg\",apb_cfg.master%s_cfg);"%(i,i))
                        # StrStr.append("uvm_config_db#(apb_cust_config)::set(this,\"apb_system_master%s_env\",\"cfg\",apb_cfg.master%s_cfg);"%(i,i))
                        StrStr.append("apb_system_master%s_env=svt_%s_system_env::type_id::create(\"apb_system_master%s_env\",this);"%(i,vipname,i))
                    for i in range(self.VIP_DB['APB']['VipSlaveNum']):
                        StrStr.append("uvm_config_db#(svt_apb_system_configuration)::set(this,\"apb_system_slave%s_env\",\"cfg\",apb_cfg.slave%s_cfg);"%(i,i))
                        # StrStr.append("uvm_config_db#(apb_cust_config)::set(this,\"apb_system_slave%s_env\",\"cfg\",apb_cfg.slave%s_cfg);"%(i,i))
                        StrStr.append("apb_system_slave%s_env=svt_%s_system_env::type_id::create(\"apb_system_slave%s_env\",this);"%(i,vipname,i))
                # AHB
                if(VipName=='AHB'):
                    StrStr.append("uvm_config_db#(svt_%s_system_configuration)::set(this,\"%s_system_env\",\"cfg\",%s_cfg.%s_cfg);" %(vipname,vipname,vipname,vipname)) 
                    StrStr.append("%s_system_env=svt_%s_system_env::type_id::create(\"%s_system_env\",this);"                       %(vipname,vipname,vipname))
                # AXI
                if(VipName=='AXI'):
                    StrStr.append("uvm_config_db#(svt_%s_system_configuration)::set(this,\"%s_system_env\",\"cfg\",%s_cfg.%s_cfg);" %(vipname,vipname,vipname,vipname))   
                    StrStr.append("%s_system_env=svt_%s_system_env::type_id::create(\"%s_system_env\",this);"                       %(vipname,vipname,vipname))    
                    StrStr.append("%s_system_env.set_report_severity_id_action_hier(UVM_INFO,\"connect_ph\",UVM_NO_ACTION);"        %(vipname))            
                StrStr.append("")
                StrStr.append("`endif")
        #top
        StrStr.append("%s_cfg    =%s_config::type_id::create(\"%s_cfg\",this);"                  %(self.tb_name,self.tb_name,self.tb_name))
        StrStr.append("%s_evt    =%s_event::type_id::create(\"%s_evt\",this);"                   %(self.tb_name,self.tb_name,self.tb_name))
        StrStr.append("%s_vseqr  =%s_virtual_sequencer::type_id::create(\"%s_vseqr\",this);"     %(self.tb_name,self.tb_name,self.tb_name))
        StrStr.append("%s_scb    =%s_scoreboard::type_id::create(\"%s_scb\",this);"              %(self.tb_name,self.tb_name,self.tb_name))
        StrStr.append("")
        #uvc agent
        for i in range(len(self.DUT_GroupName)):
            if self.DUT_VIP[i]==True:StrStr.append("`ifndef NO_%s_CUSTOM"%self.DUT_GroupName[i])
            StrStr.append("%s_agt =%s_agent::type_id::create(\"%s_agt\",this);"%(self.DUT_GroupName[i],self.DUT_GroupName[i],self.DUT_GroupName[i]))
            if self.DUT_VIP[i]==True:StrStr.append("`endif")
        # StrStr.append("")
        # for i in range(len(self.DUT_GroupName)):
        #     if self.DUT_VIP[i]==True:StrStr.append("`ifndef NO_%s_CUSTOM"%self.DUT_GroupName[i])
        #     StrStr.append("%s_agt.is_active=UVM_ACTIVE;"%self.DUT_GroupName[i])
        #     if self.DUT_VIP[i]==True:StrStr.append("`endif")
        StrStr.append("")
        StrStr.append("uvm_config_db#(%s_config)::set(null,\"\",\"%s_config\",%s_cfg);"   %(self.tb_name,self.tb_name,self.tb_name))
        StrStr.append("uvm_config_db#(%s_event)::set(null,\"\",\"%s_event\",%s_evt);"     %(self.tb_name,self.tb_name,self.tb_name))
        gen_uvm_phase(self,filename,'build_phase'  ,StrStr,Parameters.PrintEnable)

        # #[phase]:connect_phase
        # filename.write("\tvirtual function void connect_phase(uvm_phase phase);\n")
        # filename.write("\t\tsuper.connect_phase(phase);\n")
        # filename.write("\n")
        # # #vip
        # # #if self.vip_apb_enable:
        # # if self.VIP_DB['APB']['Enable']:
        # #     #for i in range(self.VIP_apb_master_num):
        # #     for i in range(self.VIP_DB['APB']['VipMasterNum']):
        # #         filename.write("\t\t%s_vseqr.apb_master_seqr_%s=apb_system_env.master[%s].sequencer;\n"
        # #                                 %(self.tb_name,i,i))
        # #     #for i in range(self.VIP_apb_slave_num):
        # #     for i in range(self.VIP_DB['APB']['VipSlaveNum']):
        # #         filename.write("\t\t%s_vseqr.apb_slave_seqr_%s=apb_system_env.slave[%s].sequencer;\n"
        # #                                 %(self.tb_name,i,i))
        # # filename.write("\n")
        # # #if self.vip_ahb_enable:
        # # if self.VIP_DB['AHB']['Enable']:
        # #     #for i in range(self.VIP_ahb_master_num):
        # #     for i in range(self.VIP_DB['AHB']['VipMasterNum']):
        # #         filename.write("\t\t%s_vseqr.ahb_master_seqr_%s=ahb_system_env.master[%s].sequencer;\n"
        # #                                 %(self.tb_name,i,i))
        # #     #for i in range(self.VIP_ahb_slave_num):
        # #     for i in range(self.VIP_DB['AHB']['VipSlaveNum']):
        # #         filename.write("\t\t%s_vseqr.ahb_slave_seqr_%s=ahb_system_env.slave[%s].sequencer;\n"
        # #                                 %(self.tb_name,i,i))
        # # filename.write("\n")
        # # #if self.vip_axi_enable:
        # # if self.VIP_DB['AXI']['Enable']:
        # #     #for i in range(self.VIP_axi_master_num):
        # #     for i in range(self.VIP_DB['AXI']['VipMasterNum']):
        # #         filename.write("\t\t%s_vseqr.axi_master_seqr_%s=axi_system_env.master[%s].sequencer;\n"
        # #                                 %(self.tb_name,i,i))
        # #     #for i in range(self.VIP_axi_slave_num):
        # #     for i in range(self.VIP_DB['AXI']['VipSlaveNum']):
        # #         filename.write("\t\t%s_vseqr.axi_slave_seqr_%s=axi_system_env.slave[%s].sequencer;\n"
        # #                                 %(self.tb_name,i,i))
        # # filename.write("\n")
        # for VipName in self.VIP_DB.keys():
        #     if self.VIP_DB[VipName]['Enable']:
        #         vipname=VipName.lower()
        #         for i in range(self.VIP_DB[VipName]['VipMasterNum']):
        #             filename.write("\t\t%s_vseqr.%s_master_seqr_%s=%s_system_env.master[%s].sequencer;\n"
        #                                     %(self.tb_name,vipname,i,vipname,i))
        #         for i in range(self.VIP_DB[VipName]['VipSlaveNum']):
        #             filename.write("\t\t%s_vseqr.%s_slave_seqr_%s=%s_system_env.slave[%s].sequencer;\n"
        #                                     %(self.tb_name,vipname,i,vipname,i))
                               
        # #uvc agent
        # for i in range(len(self.DUT_GroupName)):
        #     if self.DUT_VIP[i]==False:
        #         filename.write("\t\t%s_agt.%s_mon.mon_analysis_port.connect(%s_scb.%s_analysis_fifo.analysis_export)\n"
        #                                 %(self.DUT_GroupName[i],self.DUT_GroupName[i],self.tb_name,self.DUT_GroupName[i]))
        # filename.write("\n")
        # filename.write("\tendfunction\n")
        # filename.write("\n")
        
        StrStr=[]
        for VipName in self.VIP_DB.keys():
            if self.VIP_DB[VipName]['Enable']:
                vipname=VipName.lower()
                # for i in range(self.VIP_DB[VipName]['VipMasterNum']):
                #     StrStr.append("%s_vseqr.%s_master_seqr_%s=%s_system_env.master[%s].sequencer;"
                #                             %(self.tb_name,vipname,i,vipname,i))
                # for i in range(self.VIP_DB[VipName]['VipSlaveNum']):
                #     StrStr.append("%s_vseqr.%s_slave_seqr_%s=%s_system_env.slave[%s].sequencer;"
                #                             %(self.tb_name,vipname,i,vipname,i))
                StrStr.append("`ifndef NO_%s_VIP"%VipName)
                for i in range(self.VIP_DB[VipName]['VipMasterNum']):
                    StrStr.append("%s_vseqr.%s_master_seqr_%s=apb_system_master%s_env.sequencer;"   %(self.tb_name,vipname,i,i))
                for i in range(self.VIP_DB[VipName]['VipSlaveNum']):
                    StrStr.append("%s_vseqr.%s_slave_seqr_%s=apb_system_slave%s_env.sequencer;"   %(self.tb_name,vipname,i,i))
                StrStr.append("`endif")
        #uvc agent
        for i in range(len(self.DUT_GroupName)):
            if self.DUT_VIP[i]==True:StrStr.append("`ifndef NO_%s_CUSTOM"%self.DUT_GroupName[i])
            StrStr.append("%s_agt.%s_mon.mon_analysis_port.connect(%s_scb.%s_analysis_fifo.analysis_export);"
                                    %(self.DUT_GroupName[i],self.DUT_GroupName[i],self.tb_name,self.DUT_GroupName[i]))
            if self.DUT_VIP[i]==True:StrStr.append("`endif")
        StrStr.append("")
        # agt.vseqr
        for i in range(len(self.DUT_GroupName)):
            if self.DUT_VIP[i]==True:StrStr.append("`ifndef NO_%s_CUSTOM"%self.DUT_GroupName[i])
            StrStr.append("%s_vseqr.%s_seqr=%s_agt.%s_seqr;"%(self.tb_name,self.DUT_GroupName[i],self.DUT_GroupName[i],self.DUT_GroupName[i]))
            if self.DUT_VIP[i]==True:StrStr.append("`endif")

        gen_uvm_phase(self,filename,'connect_phase'  ,StrStr,Parameters.PrintEnable)
               
        # #[phase]:end_of_elaboration_phase
        # filename.write("\tvirtual function void end_of_elaboration_phase(uvm_phase phase);\n")
        # filename.write("\t\tsuper.end_of_elaboration_phase(phase)\n")
        # # #if self.vip_apb_enable:
        # # if self.VIP_DB['APB']['Enable']:
        # #     #for i in range(self.VIP_apb_master_num):
        # #     for i in range(self.VIP_DB['APB']['VipMasterNum']):
        # #         filename.write("\t\tapb_system_env.master[%s].set_report_severity_action(UVM_INFO,UVM_NO_ACTION)\n"%i)
        # #     #for i in range(self.VIP_apb_slave_num):
        # #     for i in range(self.VIP_DB['APB']['VipSlaveNum']):
        # #         filename.write("\t\tapb_system_env.slave[%s].set_report_severity_action(UVM_INFO,UVM_NO_ACTION)\n"%i)
        # # #if self.vip_ahb_enable:
        # # if self.VIP_DB['AHB']['Enable']:
        # #     #for i in range(self.VIP_ahb_master_num):
        # #     for i in range(self.VIP_DB['AHB']['VipMasterNum']):
        # #         filename.write("\t\tahb_system_env.master[%s].set_report_severity_action(UVM_INFO,UVM_NO_ACTION)\n"%i)
        # #     #for i in range(self.VIP_ahb_slave_num):
        # #     for i in range(self.VIP_DB['AHB']['VipSlaveNum']):
        # #         filename.write("\t\tahb_system_env.slave[%s].set_report_severity_action(UVM_INFO,UVM_NO_ACTION)\n"%i)
        # # #if self.vip_axi_enable:
        # # if self.VIP_DB['AXI']['Enable']:
        # #     #for i in range(self.VIP_axi_master_num):
        # #     for i in range(self.VIP_DB['AXI']['VipMasterNum']):
        # #         filename.write("\t\taxi_system_env.master[%s].set_report_severity_action(UVM_INFO,UVM_NO_ACTION)\n"%i)
        # #     #for i in range(self.VIP_axi_slave_num):
        # #     for i in range(self.VIP_DB['AXI']['VipSlaveNum']):
        # #         filename.write("\t\taxi_system_env.slave[%s].set_report_severity_action(UVM_INFO,UVM_NO_ACTION)\n"%i)
        # for VipName in self.VIP_DB.keys():
        #     if self.VIP_DB[VipName]['Enable']:
        #         vipname=VipName.lower()
        #         for i in range(self.VIP_DB[VipName]['VipMasterNum']):
        #             filename.write("\t\t%s_system_env.master[%s].set_report_severity_action(UVM_INFO,UVM_NO_ACTION)\n"%(vipname,i))
        #         for i in range(self.VIP_DB[VipName]['VipSlaveNum']):
        #             filename.write("\t\t%s_system_env.slave[%s].set_report_severity_action(UVM_INFO,UVM_NO_ACTION)\n"%(vipname,i))
                    
        # filename.write("\n")
        # filename.write("\tendfunction\n")
        # filename.write("\n")

        StrStr=[]
        for VipName in self.VIP_DB.keys():
            if self.VIP_DB[VipName]['Enable']:
                vipname=VipName.lower()
                # for i in range(self.VIP_DB[VipName]['VipMasterNum']):
                #     StrStr.append("%s_system_env.master[%s].set_report_severity_action(UVM_INFO,UVM_NO_ACTION);"%(vipname,i))
                # for i in range(self.VIP_DB[VipName]['VipSlaveNum']):
                #     StrStr.append("%s_system_env.slave[%s].set_report_severity_action(UVM_INFO,UVM_NO_ACTION);"%(vipname,i))
                StrStr.append("`ifndef NO_%s_VIP"%VipName)
                for i in range(self.VIP_DB[VipName]['VipMasterNum']):
                    StrStr.append("apb_system_master%s_env.set_report_severity_action(UVM_INFO,UVM_NO_ACTION);"%i)
                for i in range(self.VIP_DB[VipName]['VipSlaveNum']):
                    StrStr.append("apb_system_slave%s_env.set_report_severity_action(UVM_INFO,UVM_NO_ACTION);"%i)
                StrStr.append("`endif")
                # ===== end_of_elaboration_phase 增强 =====
        StrStr=[]
        StrStr.append("// 在此 phase 中推荐：1) 降低 VIP 日志级别  2) lock register model  3) factory override")
        gen_uvm_phase(self,filename,'end_of_elaboration_phase'  ,StrStr,Parameters.PrintEnable)

        gen_uvm_phase(self,filename,'start_of_simulation_phase' ,None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'run_phase'                 ,None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'extract_phase'             ,None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'check_phase'               ,None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'report_phase'              ,None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'final_phase'               ,None,Parameters.PrintEnable)

        # #[phase]:start_of_simulation_phase
        # filename.write("\tvirtual function void start_of_simulation_phase(uvm_phase phase);\n")
        # filename.write("\t\tsuper.start_of_simulation_phase(phase);\n")
        # filename.write("\tendfunction\n")
        # filename.write("\n")
        # #[phase]:run_phase
        # filename.write("\t//run_phase\n")
        # filename.write("\t//<pre_/post_/reset_phase><pre_/post_/configure_phase><pre_/post_/main_phase><pre_/post_/shutdown_phase>\n")
        # filename.write("\tvirtual task reset_phase(uvm_phase phase);\n")
        # filename.write("\t\tsuper.reset_phase(phase);\n")
        # filename.write("\t\tphase.raise_objection(this,\"Resetting\");\n")
        # filename.write("\t\t`ifdef REG_MODEL\n")
        # filename.write("\t\t//regmodel.reset();\n")
        # filename.write("\t\t`endif\n")
        # filename.write("\t\tphase.drop_objection(this);\n")
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

        filename.write("\n")
        filename.write("endclass\n")
        filename.write("\n")
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
    gen=gen_env_env()