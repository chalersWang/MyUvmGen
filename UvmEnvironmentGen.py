#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-

import os
import sys
import time

# Auto-detect MY_TOOLS_HOME if not set in environment
if "MY_TOOLS_HOME" not in os.environ:
    os.environ["MY_TOOLS_HOME"] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append("%s"%os.environ.get("MY_TOOLS_HOME"))

from readexcel.readexcel_WorkingDirectoryGen import readexcel_WorkingDirectoryGen
from readexcel.readexcel_VIP import readexcel_VIP
from readexcel.readexcel_ClockRst import readexcel_ClockRst
from readexcel.readexcel_DutSignal import readexcel_DutSignal
from readexcel.readexcel_RegMem import readexcel_RegMem

from gen_DirectorysStructure.gen_DirectoryStructure import gen_DirectoryStructure

from gen_cfg.gen_cfg_basecfg import gen_cfg_basecfg
from gen_cfg.gen_cfg_utcfg import gen_cfg_utcfg
from gen_cfg.gen_cfg_itcfg import gen_cfg_itcfg
from gen_cfg.gen_cfg_stcfg import gen_cfg_stcfg

from gen_filelist.gen_filelist_file import gen_filelist_file

# from gen_tb_crg import gen_tb_crg
# from gen_tb_dutinst import gen_tb_dutinst
# from gen_tb_uvmconfigdb import gen_tb_uvmconfigdb
# from gen_tb_dumpctrl import gen_tb_dumpctrl
from gen_tb.gen_tb_top      import gen_tb_top

from gen_env.gen_env_EnvTop import gen_env_EnvTop
from gen_env.gen_env_env import gen_env_env
from gen_env.gen_env_virtual_sequencer import gen_env_virtual_sequencer
from gen_env.gen_env_scoreboard import gen_env_scoreboard
from gen_env.gen_env_function_coverage import gen_env_function_coverage

from gen_uvc.gen_uvc_UvcTop import gen_uvc_UvcTop
from gen_uvc.gen_uvc_agent import gen_uvc_agent
from gen_uvc.gen_uvc_driver import gen_uvc_driver
from gen_uvc.gen_uvc_monitor import gen_uvc_monitor
from gen_uvc.gen_uvc_sequencer import gen_uvc_sequencer
from gen_uvc.gen_uvc_trans import gen_uvc_trans
from gen_uvc.gen_uvc_sequence_lib import gen_uvc_sequence_lib
from gen_uvc.gen_uvc_vif import gen_uvc_vif

from gen_uvc.gen_apb_uvc import gen_apb_uvc
from gen_uvc.gen_ahb_uvc import gen_ahb_uvc
from gen_uvc.gen_axi_uvc import gen_axi_uvc

from gen_testcase.gen_testcase_TestTop import gen_testcase_TestTop
from gen_testcase.gen_testcase_sequence_lib import gen_testcase_sequence_lib
from gen_testcase.gen_testcase_base_test import gen_testcase_base_test
from gen_testcase.gen_testcase_demo_test import gen_testcase_demo_test

from gen_coverage.gen_coverage_file import gen_coverage_file
from gen_sva.gen_sva_file import gen_sva_file
from gen_sva.gen_define_file import gen_define_file
from gen_tcl.gen_tcl_file import gen_tcl_file
from gen_run.gen_run_file import gen_run_file

from gen_common.gen_common_config import gen_common_config
from gen_common.gen_common_event import gen_common_event

from gen_readme.gen_readme import gen_readme
from gen_sourceme.gen_sourceme import gen_sourceme
from gen_json.gen_json_file import gen_json_file
from gen_testplan.gen_testplan_file import gen_testplan_file

# ===== Register Model 模块 =====
from gen_regmodel.gen_reg_block import gen_reg_block
from gen_regmodel.gen_reg_adapter import gen_reg_adapter
from gen_regmodel.gen_reg_sequence import gen_reg_sequence

from common_lib.common_lib import CopyFile
from common_lib.common_lib import DoScript
from common_lib.parameters import Parameters
from common_lib.numbers_converter import convert_numbers_if_needed

script_path=os.path.split(os.path.realpath(__file__))[0]
print("[Script] : %s [Path]: %s"%(os.path.basename(__file__),script_path))
#print("welcome to generating verify environment!!")

class Uvm_Environment_Gen:
    def __init__(self,tbname,EnvironmentGenCfg):
        #self.tb_name=tbname
        self.EnvironmentGenCfg=EnvironmentGenCfg
        self.local_dir = os.getcwd()
        os.chdir(self.local_dir+'/')

    def readexcel(self):        
        print("read EnvironmentGenCfg.xlsx")
        self.StrStrStr=[]
        self.ReadexcelWorkingDirectoryGen()
        self.ReadExcelVIP()
        self.ReadExcelClockRst()
        self.ReadExcelDutSignal()
        self.ReadExcelRegMem()

    def ReadexcelWorkingDirectoryGen(self):      
       readexcel_WorkingDirectoryGen.readexcel_WorkingDirectoryGen_info(self,EnvironmentGenCfg,PrintEnable=False)
    
    def ReadExcelVIP(self):      
        readexcel_VIP.readexcel_VIP_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_VIP.readexcel_VIP_AXI_info(self,EnvironmentGenCfg,PrintEnable=False)

    def ReadExcelClockRst(self):      
        readexcel_ClockRst.readexcel_ClockRst_info(self,EnvironmentGenCfg,PrintEnable=False)

    def ReadExcelDutSignal(self):      
        readexcel_DutSignal.readexcel_DutSignal_info(self,EnvironmentGenCfg,PrintEnable=False)
    
    def ReadExcelRegMem(self):      
        readexcel_RegMem.readexcel_RegMem_info(self,EnvironmentGenCfg,PrintEnable=False)
    
    def gen_tb_dir(self):
        gen_DirectoryStructure.gen_DirectoryStructure_info(self,self.local_dir,self.tb_name,PrintEnable=False)

    def gen_cfg_file(self):
        os.chdir(self.local_dir+'/'+'cfg')
        # base.cfg
        gen_cfg_basecfg.gen_cfg_basecfg_info(self,PrintEnable=False)
        # # ut_xx.cfg
        # if self.ut_xx_cfg_enable :
        #     gen_cfg_utcfg.gen_cfg_utcfg_info(self,PrintEnable=False)
        # # it_xx.cfg
        # if self.it_xx_cfg_enable :
        #     gen_cfg_itcfg.gen_cfg_itcfg_info(self,PrintEnable=False)
        # # st_xx.cfg
        # if self.st_xx_cfg_enable :
        #     gen_cfg_stcfg.gen_cfg_stcfg_info(self,PrintEnable=False)
    
    def gen_filelist_file(self):
        os.chdir(self.local_dir+'/'+'filelist')
        gen_filelist_file.gen_filelist_file_info(self,self.tb_name,self.DUT_GroupName,PrintEnable=False)

    def gen_tb_file(self):
        os.chdir(self.local_dir+'/'+'tb')
        gen_tb_top.gen_tb_top_info(self,self.tb_name,PrintEnable=False)

    def gen_env_file(self):
        os.chdir(self.local_dir+'/'+'env')
        #xx_EnvTop.sv
        self.gen_xx_EnvTop()
        #xx_env.sv
        self.gen_xx_env()
        #xx_virtual_sequencer.sv
        self.gen_xx_virtual_sequencer()
        #xx_scoreboard.sv
        self.gen_xx_scoreboard()
        #xx_function_coverage.sv
        self.gen_xx_function_coverage()
        #xx_config.sv
        self.gen_xx_config()
        #xx_event.sv
        self.gen_xx_event()
    
    def gen_xx_EnvTop(self):
        gen_env_EnvTop.gen_env_EnvTop_info(self,PrintEnable=False)
    
    def gen_xx_env(self):
        gen_env_env.gen_env_env_info(self,PrintEnable=False)
    
    def gen_xx_virtual_sequencer(self):
        gen_env_virtual_sequencer.gen_env_virtual_sequencer_info(self,PrintEnable=False)
    
    def gen_xx_scoreboard(self):
        gen_env_scoreboard.gen_env_scoreboard_info(self,PrintEnable=False)

    def gen_xx_function_coverage(self):
       gen_env_function_coverage.gen_env_function_coverage_info(self,PrintEnable=False)
    
    def gen_xx_config(self):
        gen_common_config.gen_common_config_info(self,self.tb_name,PrintEnable=False)
        
    def gen_xx_event(self):
       gen_common_event.gen_common_event_info(self,self.tb_name,PrintEnable=False)
      
    def gen_coverage_file(self):
        os.chdir(self.local_dir+'/'+'coverage/code')
        gen_coverage_file.gen_coverage_file_info(self,PrintEnable=False)

    def gen_sva_file(self):
        os.chdir(self.local_dir+'/'+'sva')
        gen_define_file.gen_define_file_info(self,PrintEnable=False)
        gen_sva_file.gen_sva_file_info(self,PrintEnable=False)

    def gen_tcl_file(self):
        os.chdir(self.local_dir+'/'+'tcl')
        gen_tcl_file.gen_tcl_file_info(self,None,PrintEnable=False)
    
    def gen_run_file(self):
        os.chdir(self.local_dir+'/'+'run')
        #gen_run_file.gen_run_file_info(self,PrintEnable=False)
        if(Parameters.runscript=="run"):
            gen_run_file.gen_run_file_info(self,'run',PrintEnable=False)
            gen_run_file.gen_makefile_file_info(self,'Makefile',PrintEnable=False)
        elif(Parameters.runscript=="xrun"):
            gen_run_file.gen_xrun_file_info(self,'xrun',PrintEnable=False)
        else:
            gen_run_file.gen_run_file_info(self,'run',PrintEnable=False)
            gen_run_file.gen_xrun_file_info(self,'xrun',PrintEnable=False)
            gen_run_file.gen_makefile_file_info(self,'Makefile',PrintEnable=False)
    
    def gen_json_file(self):
        os.chdir(self.local_dir+'/'+'json')
        os.getcwd()
        script  ='excel_to_json'
        cfgfile ="%s_VerifyPlan.xlsx"%self.tb_name
        #gen_json_file.gen_json_file_info(self,jsonname='excel_to_json',PrintEnable=False)
        gen_json_file.gen_json_file_info(self,jsonname=script,PrintEnable=False)
        ##CopyFile(self,"%s/gen_json/VerifyPlan.xlsx"%os.path.split(os.path.realpath(__file__))[0],self.local_dir+'/'+'json')
        #CopyFile(self,"%s\gen_json\VerifyPlan.xlsx"%script_path,self.local_dir+'\\'+'json\%s_VerifyPlan.xlsx'%self.tb_name)
        
        CopyFile(self,os.path.join(script_path,"gen_json","VerifyPlan.xlsx"),os.path.join(self.local_dir,"json","%s"%cfgfile))
        #CopyFile(self,"%s\gen_json\VerifyPlan.xlsx"%script_path,self.local_dir+Parameters.slash+'json\%s'%cfgfile)
        #DoScript(self,script+'.py',cfgfile)
        import subprocess
        subprocess.run([sys.executable, script+'.py', '-excel', cfgfile, '-sheet', 'CaseList', '-vsqr', self.tb_name+'_vseqr', '-wave', '$VERIFY_HOME/tcl/wave.tcl'])

    def gen_testplan_file(self):
        os.chdir(self.local_dir+'/'+'testplan')
        gen_testplan_file.gen_testplan_file_info(self,self.local_dir+'/'+'json',self.local_dir+'/'+'filelist',PrintEnable=False)
        #os.system('rm -rf %s/json/*.json'%self.local_dir)
        
        os.chdir(self.local_dir+'/'+'json')
        import glob, platform
        for f in glob.glob('*.json'):
            os.remove(f)

    def gen_uvc_file(self):
        os.chdir(self.local_dir+'/'+'uvc')
        for i in range(len(self.DUT_GroupName)):
            #[not vip]:
            # if self.DUT_VIP[i]==False:
                os.chdir(self.local_dir+'/'+'uvc')
                if not os.path.isdir('%s'%self.DUT_GroupName[i]):
                    os.mkdir('%s'%self.DUT_GroupName[i])
                os.chdir('%s'%self.DUT_GroupName[i])
                #UvcTop
                self.gen_uvc_UvcTop(self.DUT_GroupName[i])
                #agent
                self.gen_uvc_agent(self.DUT_GroupName[i])
                #driver
                self.gen_uvc_driver(self.DUT_GroupName[i],self.DUT_Signals[i])
                #monitor
                self.gen_uvc_monitor(self.DUT_GroupName[i],self.DUT_Signals[i])
                #sequencer
                self.gen_uvc_sequencer(self.DUT_GroupName[i])
                #trans
                self.gen_uvc_trans(self.DUT_GroupName[i],self.DUT_Signals[i])
                #sequence_lib
                self.gen_uvc_sequence_lib(self.DUT_GroupName[i])
                #virtual interface
                self.gen_uvc_vif(self.DUT_GroupName[i],self.DUT_Signals[i])
                #config
                gen_common_config.gen_common_config_info(self,self.DUT_GroupName[i],PrintEnable=False)
        
        #[vip]:
        for VipName in self.VIP_DB.keys():
            if self.VIP_DB[VipName]['Enable']:
                os.chdir(self.local_dir+'/'+'uvc')
                # if not os.path.isdir(VipName.lower()+'_vip'):
                if not os.path.isdir(VipName+'_vip'):
                    os.mkdir(VipName+'_vip')
                os.chdir(VipName+'_vip')

                if VipName=='APB':
                    gen_apb_uvc.gen_apb_uvc_info(self,PrintEnable=False)
                
                if VipName=='AHB':
                    gen_ahb_uvc.gen_ahb_uvc_info(self,PrintEnable=False)

                if VipName=='AXI':
                    gen_axi_uvc.gen_axi_uvc_info(self,PrintEnable=False)

    def gen_uvc_UvcTop(self,name):
        gen_uvc_UvcTop.gen_uvc_UvcTop_info(self,name,PrintEnable=False)

    def gen_uvc_agent(self,name):
        gen_uvc_agent.gen_uvc_agent_info(self,name,PrintEnable=False)
    
    def gen_uvc_driver(self,name,SIGNALS):
        gen_uvc_driver.gen_uvc_driver_info(self,name,SIGNALS,PrintEnable=False)
        
    def gen_uvc_monitor(self,name,SIGNALS):
        gen_uvc_monitor.gen_uvc_monitor_info(self,name,SIGNALS,PrintEnable=False)
    
    def gen_uvc_sequencer(self,name):
        gen_uvc_sequencer.gen_uvc_sequencer_info(self,name,PrintEnable=False)

    def gen_uvc_trans(self,name,SIGNALS):
        gen_uvc_trans.gen_uvc_trans_info(self,name,SIGNALS,PrintEnable=False)
    
    def gen_uvc_sequence_lib(self,name):
        gen_uvc_sequence_lib.gen_uvc_sequence_lib_info(self,name,PrintEnable=False)
    
    def gen_uvc_vif(self,name,SIGNALS):
        gen_uvc_vif.gen_uvc_vif_info(self,name,SIGNALS,PrintEnable=False)

    def gen_testcase_file(self):
        os.chdir(self.local_dir+'/'+'testcase')
        #xx_TestTop.svh
        self.gen_testcase_TestTop(self.tb_name)
        
        #xx_sequence_lib.sv
        if not os.path.isdir('sequence_lib'):
            os.mkdir('sequence_lib')
        os.chdir('sequence_lib')
        self.gen_testcase_sequencelib(self.tb_name)
        os.chdir(self.local_dir+'/'+'testcase')
        #self.gen_testcase_uvc_sequencelib(self)

        #xx_base_test.sv
        self.gen_base_test(self.tb_name)

    def gen_testcase_TestTop(self,name):
        gen_testcase_TestTop.gen_testcase_TestTop_info(self,name,PrintEnable=False)
    
    def gen_testcase_sequencelib(self,name):
        gen_testcase_sequence_lib.gen_testcase_sequence_lib_info(self,name,PrintEnable=False)

    def gen_base_test(self,name):
        gen_testcase_base_test.gen_testcase_base_test_info(self,name,self.DUT_GroupName,PrintEnable=False)
        gen_testcase_demo_test.gen_testcase_demo_test_info(self,name,PrintEnable=False)
    
    # ========== Register Model 生成 ==========
    def gen_reg_model_file(self):
        """
        生成 UVM Register Model (RAL):
        - xx_reg_block.sv: 寄存器块定义（含每个寄存器的 uvm_reg 类）
        - xx_reg_adapter.sv: 总线适配器 (uvm_reg_adapter)
        - xx_reg_sequence.sv: 寄存器自测试 sequence
        
        若 RegModel Sheet 中无数据，则跳过。
        """
        if not hasattr(self, 'REG_Name') or not self.REG_Name:
            print("[gen_reg_model] 无寄存器定义，跳过 RAL 生成")
            return
        
        os.makedirs(os.path.join(self.local_dir, 'regmodel'), exist_ok=True)
        os.chdir(os.path.join(self.local_dir, 'regmodel'))
        
        # 1. 生成 register block (uvm_reg + uvm_reg_block)
        gen_reg_block.gen_reg_block_info(self, self.tb_name, PrintEnable=False)
        
        # 2. 生成 reg_adapter（使用第一个非 VIP 的 DUT group 作为总线名）
        bus_name = self.tb_name
        if hasattr(self, 'DUT_GroupName') and self.DUT_GroupName:
            for i in range(len(self.DUT_GroupName)):
                if not self.DUT_VIP[i]:
                    bus_name = self.DUT_GroupName[i]
                    break
        gen_reg_adapter.gen_reg_adapter_info(self, bus_name, PrintEnable=False)
        
        # 3. 生成寄存器自测试 sequence
        gen_reg_sequence.gen_reg_sequence_info(self, self.tb_name, PrintEnable=False)
        
        print("[gen_reg_model] 寄存器模型已生成: regmodel/")
        print("  - %s_reg_block.sv" % self.tb_name)
        print("  - %s_reg_adapter.sv" % bus_name)
        print("  - %s_reg_sequence.sv" % self.tb_name)

    def Gen_ReadMe(self):
        gen_readme.gen_readme_file(self,self.local_dir)
    
    def Gen_SourceMe(self):
        gen_sourceme.gen_sourceme_file(self,self.local_dir,PrintEnable=False)

    #===================================================================================

def main(tbname,EnvironmentGenCfg):
    # start cfg
    UvmEnvironmentGen=Uvm_Environment_Gen(tbname,EnvironmentGenCfg)
    UvmEnvironmentGen.readexcel()
    UvmEnvironmentGen.gen_tb_dir()
    UvmEnvironmentGen.gen_cfg_file()
    UvmEnvironmentGen.gen_filelist_file()
    UvmEnvironmentGen.gen_tb_file()
    UvmEnvironmentGen.gen_env_file()
    UvmEnvironmentGen.gen_coverage_file()
    UvmEnvironmentGen.gen_sva_file()
    UvmEnvironmentGen.gen_tcl_file()
    UvmEnvironmentGen.gen_uvc_file()
    UvmEnvironmentGen.gen_testcase_file()
    UvmEnvironmentGen.gen_run_file()
    UvmEnvironmentGen.Gen_ReadMe()
    UvmEnvironmentGen.Gen_SourceMe()
    UvmEnvironmentGen.gen_reg_model_file()  # 寄存器模型（含自测试 sequence）
    UvmEnvironmentGen.gen_json_file()
    UvmEnvironmentGen.gen_testplan_file()


if __name__ == '__main__':
    # initial cfg
    tbname=Parameters.tb_name
    EnvironmentGenCfg=Parameters.EnvironmentGenCfg
    # judge where there is a VerifyEnvironmentGenCfg file 
    if len(sys.argv) == 1:
        EnvironmentGenCfg = input('Please input excel file name:\n')
    else:
        EnvironmentGenCfg = sys.argv[1]
    # Auto-convert .numbers → .xlsx if needed
    if EnvironmentGenCfg.endswith('.numbers'):
        EnvironmentGenCfg = convert_numbers_if_needed(EnvironmentGenCfg)

    if EnvironmentGenCfg.strip() == '':
        print("\nError: No excel file name provided !!!")
        print("Program terminated ...")
        time.sleep(3)
        raise Exception("No excel file name provided !!!")
    if not os.path.exists(EnvironmentGenCfg):
        print("\nError: No excel file name provided !!!")
        print("Program terminated ...")
        time.sleep(3)
        raise Exception("No excel file name provided !!!")
    
    main(tbname,EnvironmentGenCfg)
   
   
