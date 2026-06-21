#! /usr/bin/env python
# -*-coding:UTF-8-*-
import argparse
import os
import sys
import re
import json
import random
import threading
import time
import datetime
import smtplib
from multiprocessing import Process, Pool
import subprocess
from email.mime.text import MIMEText
from email.header import Header

script_path=os.path.split(os.path.realpath(__file__))[0]
print("[Script Path]: %s"%script_path)
# print("[Script] : %s [Path]: %s"%(__file__.split('\\')[-1],script_path))

class TestCase(object):
    pass

class xrun(object):

    def __init__(self):
        self.base_compile_opt   =[]
        self.base_simulation_opt=[]
        self.testgroup_list     =[]
        self.test_define_list   =[]
        self.test_rtl_list      =[]
        self.test_tb_list       =[]
        self.test_vip_list      =[]
        self.test_cmodel_list   =[]
        self.resultlog          =""" """
        self.regressionlog      =""" """
        self.PrintLog("[xrun]: initial",False)
        self.GetArgs()
        self.GetEnv()
        self.GetTestcaseList()
    
    def GetArgs(self):
        self.PrintLog("[xrun]: GetArgs",False)
        parser = argparse.ArgumentParser(description='EzChip Testbench Flow Args Parser')
        parser.add_argument('-t', '--test',             nargs="+",                      dest="testlib",                        help="give the test list that should be run")
        parser.add_argument('-g', '--group',            nargs='+',                      dest="grouplib",                       help="give the group list that should be run")
        #parser.add_argument('-v', '--verdi',           action='store_true',            dest="waveform",        default=False, help="enable dump the simulation waveform")
        parser.add_argument('-n', '--num',              action='store',     type=int,   dest="iteration_num",   default=1,      help="the iteration num of")
        parser.add_argument('-c', '--comp',             action='store_true',            dest="compile",         default=False,  help="enable compile work")
        parser.add_argument('-s', '--sim',              action='store_true',            dest="sim",             default=False,  help="enable simulation work")
        parser.add_argument('-d', '--debug',            action='store_true',            dest="debug",           default=False,  help="enable debug mode")
        parser.add_argument('-l', '--list',             action='store_true',            dest="list",            default=False,  help="list all the test")
        #parser.add_argument('--gls',                   action='store_true',            dest="gls",             efault=False,   help="Enable Gatelevel Sim")
        parser.add_argument('--cov',                    action='store_true',            dest="cov",             default=False,  help="Enable Dump Coverage")
        #parser.add_argument('--cov_opt',               nargs='+',                      dest="cov_opt",                         help="add coverage options")
        parser.add_argument('--covmerge',               action='store_true',            dest="covmerge",        default=False,  help="merge coverage")
        parser.add_argument('--opencov',                action='store',                 dest="opencov",         default=None,   help="open tne cov")
        parser.add_argument('--seed',                   action='store',                 dest="seed",            default=None,   help="give the seed")
        parser.add_argument('--log',                    action='store_true',            dest="log",             default=False,  help="open test log")
        #parser.add_argument('--check',                 action='store_true',            dest="check",           default=None,   help="check test log")
        #parser.add_argument('-m','--m',                action='store_true',            dest="email",           default=False,  help="send email")
        parser.add_argument('--clean',                  action='store_true',            dest="clean",           default=False,  help="clean test")
        #parser.add_argument('-q', '--quiet',           action='store_true',            dest="quiet",           default=False,  help="enable quiet mode")
        parser.add_argument('-fsdb', '--fsdb',          action='store_true',            dest="fsdb",            default=False,  help="enable fsdb Dump")

        parser.add_argument('--compcfg',                action='store',                 dest="compcfg",         default=None,   help="additional compile cfg file")
        parser.add_argument('--simcfg',                 action='store',                 dest="simcfg",          default=None,   help="additional simulation cfg file")
        parser.add_argument('--tcl',                    action='store',                 dest="wavetcl",        default=None,   help="additional wave.tcl file")
        parser.add_argument('-p', '--parallel',           action='store',     type=int,   dest="parallel_jobs",   default=0,      help="number of parallel simulation jobs (0=serial)")

        self.args = parser.parse_args()

        if self.args.debug:
            self.PrintEnable=True
        else:
            self.PrintEnable=False

    def GetEnv(self):
        self.PrintLog("[xrun]:GetEnv",self.PrintEnable)
        # 环境变量: 改为 fallback 默认值，不再 assert 崩溃
        env_defaults = {
            "VERIFY_HOME":    os.getcwd(),
            "TESTPLAN_HOME":  os.path.join(os.getcwd(), "testplan"),
            "TOOLS_HOME":     os.path.join(os.getcwd(), "tools"),
            "VCS_HOME":       os.path.join(os.getcwd(), "vcs"),
            "VERDI_HOME":     os.path.join(os.getcwd(), "verdi"),
        }
        for var, default in env_defaults.items():
            if var not in os.environ:
                self.PrintLog("[WARN] %s not set, using: %s" % (var, default), True)
                os.environ[var] = default
            else:
                self.PrintLog("[ENV]  %s = %s" % (var, os.environ[var]), self.PrintEnable)
            
        self.tb_home        = os.environ["VERIFY_HOME"]
        self.testplan_home  = os.environ["TESTPLAN_HOME"]

        self.build_home             = "%s/build"            %self.tb_home
        self.cfg_home               = "%s/cfg"              %self.tb_home
        self.filelist_home          = "%s/filelist"         %self.tb_home
        self.coverage_home          = "%s/coverage"         %self.tb_home
        self.coverage_result_dir    = "%s/coverage_result"  %self.coverage_home

# ****************************************************************************************************************************************
    def XrunSim(self):
        self.PrintLog("[xrun]:XrunSim",self.PrintEnable)
        if self.args.list:
            self.PrintTestcaseList()

        elif self.args.clean:
            subprocess.run(["rm","-rf",self.build_home], check=False)

        elif self.args.log:
            self.OpenSimLog()

        elif self.args.covmerge:
            self.MergeCoverage()
        
        elif self.args.opencov!=None:
            self.OpenCoverage()
        
        elif self.args.compile:
            self.DoCompile_pre(self.args.grouplib,self.args.testlib)
            self.DoCompile(self.args.grouplib,self.args.testlib)
        
        elif self.args.sim:
            if self.args.parallel_jobs > 0:
                self.DoSimParallel(self.args.grouplib, self.args.testlib)
            else:
                self.DoSimulation(self.args.grouplib,self.args.testlib)

# ****************************************************************************************************************************************
    def GetTestcaseList(self):
        self.PrintLog("[xrun]:GetTestcaseList",self.PrintEnable)
        def __AddPath(x):
            return "%(home)s/%(group)s" % ({"home": self.testplan_home, "group": x})
        for root, dirs, files in os.walk(self.testplan_home):
            self.testgroup = dirs
            if ".svn" in self.testgroup:
                self.testgroup.remove(".svn")
            break
        self.testgroup = list(map(__AddPath, self.testgroup))
        self.testdb = {}
        self.PrintArray(sorted(self.testgroup),self.PrintEnable)

        for group in self.testgroup:
            __groupname = group.split("/")[-1]
            __definefile= "%s/define.f"     %group
            __rtlfile   = "%s/rtl.f"        %group
            __tbfile    = "%s/tb.f"         %group
            __vipfile   = "%s/vip.f"        %group
            __cmodelfile= "%s/cmodel.f"     %group
            __testlist  = "%s/test.json"    %group
            assert os.path.exists(__rtlfile),   "no rtl.f in %s"    %group
            assert os.path.exists(__tbfile),    "no tb.f in %s"     %group
            assert os.path.exists(__vipfile),   "no vip.f in %s"    %group
            assert os.path.exists(__cmodelfile),"no cmodel.f in %s" %group
            assert os.path.exists(__testlist),  "no testlist in %s" %group
            self.testdb[__groupname]            = {}
            self.testdb[__groupname]["define"]  = __definefile
            self.testdb[__groupname]["rtl"]     = __rtlfile
            self.testdb[__groupname]["tb"]      = __tbfile
            self.testdb[__groupname]["vip"]     = __vipfile
            self.testdb[__groupname]["cmodel"]  = __cmodelfile
            __testfile = open(__testlist, 'r')
            try:
                __testjson = json.load(__testfile)
            except json.JSONDecodeError as e:
                self.PrintLog("[ERROR] Bad JSON in %s: %s" % (__testlist, str(e)), True)
                raise
            self.testdb[__groupname]["test"] = __testjson
            __testfile.close()

            # self.test_define_list.append(__definefile)
            # self.test_rtl_list.append(__rtlfile)
            # self.test_tb_list.append(__tbfile)
            # self.test_vip_list.append(__vipfile)
            # self.test_vcmodel_list.append(__cmodelfile)

        for group in self.testgroup:
            gg = group.split("/")[-1]
            for tt in self.testdb[gg]['test'].keys():
                for kk in self.testdb[gg]['test'][tt].keys():
                    if not isinstance(self.testdb[gg]['test'][tt][kk], dict):
                        self.testdb[gg]['test'][tt][kk] = os.path.expandvars(self.testdb[gg]['test'][tt][kk])

        if self.args.debug:
            print(self.testdb)

    def PrintTestcaseList(self):
        self.PrintLog("[xrun]:PrintTestcaseList",self.PrintEnable)
        testinfo="""
********************************************************
**          TestCase List
********************************************************"""
        groupnum=0
        for g in sorted(self.testdb.keys()):
            groupnum=groupnum+1
            testinfo+='''
group[%s]: %s'''%(groupnum,g)
            casenum=0
            for t in sorted(self.testdb[g]['test'].keys()):
                casenum=casenum+1
                testinfo+='''
    case[%s]: %s'''%(casenum,t)
        self.PrintLog(testinfo,True)

# *****************************************************************************************
    def DoCompile_pre(self,GroupName,TestName):
        self.PrintLog("[xrun]:DoCompile_pre",self.PrintEnable)
        os.chdir(self.tb_home)
        self.PrintArray(self.testgroup_list,self.PrintEnable)
        self.CreateDir('build')
        os.chdir('build')
        # no -g and no -t
        if GroupName==None and TestName==None:
            raise Exception("Give at least one grouname or testname!!!")
        # no -g and -t
        elif GroupName==None and TestName!=None:
            self.CreateDir(TestName[0])
            os.chdir(TestName[0])
            self.CreateDir('comp')
            self.CreateDir('sim')
        # -g and no -t
        elif GroupName!=None and TestName==None:
            self.CreateDir(GroupName[0])
            os.chdir(GroupName[0])
            self.CreateDir('comp')
            self.CreateDir('sim')
        # -g and -t
        elif GroupName!=None and TestName!=None:
            self.CreateDir(GroupName[0])
            os.chdir(GroupName[0])
            self.CreateDir('comp')
            self.CreateDir('sim')
            os.chdir('sim')
            self.CreateDir(TestName[0])
        
        if self.args.cov:
            self.CreateCoverageDir(GroupName,TestName)
        
        os.chdir(self.tb_home)

    def DoCompile(self,GroupName,TestName):
        self.PrintLog("[xrun]:DoCompile",self.PrintEnable) 
        self.GetBaseCompileOpt()
        Compile_dir="./"
        # no -g and no -t
        if GroupName==None and TestName==None:
            raise Exception("Give at least one grouname or testname!!!")
        # no -g and -t
        elif GroupName==None and TestName!=None:
            groupname=self.MatchGroupAccordingToCase(TestName[0])
            define_file="%s"%self.testdb[groupname]["define"]
            rtl_file="%s"%self.testdb[groupname]["rtl"]
            tb_file="%s"%self.testdb[groupname]["tb"]
            vip_file="%s"%self.testdb[groupname]["vip"]
            cmodel_file="%s"%self.testdb[groupname]["cmodel"]
            Compile_dir="%s/%s/comp"%(self.build_home,TestName[0])
            coverageresultdir="%s/%s/cov.vdb"%(self.coverage_result_dir,groupname)
        # -g and no -t | -g and -t
        else:
            define_file="%s"%self.testdb[GroupName[0]]["define"]
            rtl_file="%s"%self.testdb[GroupName[0]]["rtl"]
            tb_file="%s"%self.testdb[GroupName[0]]["tb"]
            vip_file="%s"%self.testdb[GroupName[0]]["vip"]
            cmodel_file="%s"%self.testdb[GroupName[0]]["cmodel"]
            Compile_dir="%s/%s/comp"%(self.build_home,GroupName[0])
            coverageresultdir="%s/%s/cov.vdb"%(self.coverage_result_dir,GroupName[0])
        
        if self.args.cov:
            self.base_compile_opt.append("-cm dir %s"%coverageresultdir)

        self.RunCompCmd(Compile_dir,define_file,vip_file,rtl_file,tb_file,cmodel_file)

    def RunCompCmd(self,Compile_dir,definefile,vipfile,rtlfile,tbfile,cmodelfile):
        self.PrintLog("[xrun]:RunCompCmd",self.PrintEnable) 
        self.WriteCfgFile(Compile_dir,CompSim="Comp")
        self.ReadKfile("%s"%self.filelist_home,Compile_dir+"/compile.opt",Compile_dir)
        Compile_CMD=[]
        Compile_CMD.append('vcs')
        for i in range(len(self.base_compile_opt)):
            Compile_CMD.append(self.base_compile_opt[i])
        # define.f
        if definefile!=None:
            Compile_CMD.append('-file %s'%definefile)
        # vip.k
        if self.vipkfile==True:
            Compile_CMD.append('-file %s/vip_new.f'%Compile_dir)
        else:
            Compile_CMD.append('-file %s'%vipfile)
        # rtl.k
        if self.rtlkfile==True:
            Compile_CMD.append('-file %s/rtl_new.f'%Compile_dir)
        else:
            Compile_CMD.append('-file %s'%rtlfile)
        # tb.k
        if self.tbkfile==True:
            Compile_CMD.append('-file %s/tb_new.f'%Compile_dir)
        else:
            Compile_CMD.append('-file %s'%tbfile)
        # tb.k
        if self.cmodelkfile==True:
            Compile_CMD.append('-file %s/tb_new.f'%Compile_dir)
        else:
            Compile_CMD.append('-file %s'%cmodelfile)
        
        CompileCMD=" \\\n".join(Compile_CMD)
        self.PrintLog("%s"%CompileCMD,True)
        os.chdir("%s"%Compile_dir)
        result = subprocess.run(CompileCMD, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            self.PrintLog("[ERROR] Compile failed:\n" + result.stderr[-500:], True)
            raise RuntimeError("VCS compilation failed")

# *****************************************************************************************
    def DoSimulation(self,GroupName,TestName):
        self.PrintLog("[xrun]:DoSimulation",self.PrintEnable)
        self.GetBaseSimulationOpt()
        Compile_dir     ="./"
        Simulation_dir  ="./"
        # no -g and no -t
        if GroupName==None and TestName==None:
            raise Exception("Give at least one grouname or testname!!!")
        # no -g and -t
        elif GroupName==None and TestName!=None:
            for num in range(0,self.args.iteration_num):
                SEED=self.SeedGen()
                Compile_dir="%s/%s/comp"%(self.build_home,TestName[0])
                Simulation_dir="%s/%s/sim/%s"%(self.build_home,TestName[0],SEED)
                os.chdir("%s/%s/sim"%(self.build_home,TestName[0]))
                self.CreateDir("%s"%SEED)
                groupname=self.MatchGroupAccordingToCase(TestName[0])
                self.RunSimCmd(Compile_dir,Simulation_dir,groupname,TestName[0])
                self.CheckSimLog(Compile_dir,Simulation_dir,TestName[0],SEED)
            self.PrintResultLog(Compile_dir)
        # -g and no -t
        elif GroupName!=None and TestName==None:
            for num in range(0,self.args.iteration_num):
                for testname in self.testdb[GroupName[0]]['test'].keys():
                    SEED=self.SeedGen()
                    Compile_dir="%s/%s/comp"%(self.build_home,GroupName[0])
                    Simulation_dir="%s/%s/sim/%s/%s"%(self.build_home,GroupName[0],testname,SEED)
                    os.chdir("%s/%s/sim"%(self.build_home,GroupName[0]))
                    self.CreateDir("%s"%testname)
                    os.chdir("%s"%testname)
                    self.CreateDir("%s"%SEED)
                    self.RunSimCmd(Compile_dir,Simulation_dir,GroupName[0],testname)
                    self.CheckSimLog(Compile_dir,Simulation_dir,testname,SEED)
            self.PrintResultLog(Compile_dir)
        # -g and -t
        elif GroupName!=None and TestName!=None:
            for num in range(0,self.args.iteration_num):
                SEED=self.SeedGen()
                Compile_dir="%s/%s/comp"%(self.build_home,GroupName[0])
                Simulation_dir="%s/%s/sim/%s/%s"%(self.build_home,GroupName[0],TestName[0],SEED)
                os.chdir("%s/%s/sim"%(self.build_home,GroupName[0]))
                self.CreateDir("%s"%TestName[0])
                os.chdir("%s"%TestName[0])
                self.CreateDir("%s"%SEED)
                groupname=self.MatchGroupAccordingToCase(TestName[0])
                self.RunSimCmd(Compile_dir,Simulation_dir,GroupName[0],TestName[0])
                self.CheckSimLog(Compile_dir,Simulation_dir,TestName[0],SEED)
            self.PrintResultLog(Compile_dir)

    def RunSimCmd(self,SimvDir,SimDir,GroupName,TestName):
        self.PrintLog("[xrun]:RunSimCmd",self.PrintEnable)
        Simulation_CMD=[]
        Simulation_CMD.append('%s/simv'%SimvDir)
        Simulation_CMD.append('+UVM_TESTNAME=%s'%self.testdb[GroupName]['test'][TestName]['uvm_testname'])
        coverageresultdir="%s/%s/%s.vdb"%(self.coverage_result_dir,GroupName,TestName)
        if self.args.cov:
            self.base_simulation_opt.append("-cm dir %s"%coverageresultdir)
        for i in range(len(self.base_simulation_opt)):
            Simulation_CMD.append(self.base_simulation_opt[i])
        Simulation_CMD.append('%s'%self.testdb[GroupName]['test'][TestName]['sim_args'])
        os.environ['MY_FSDB_DUMP']="off"
        if self.args.fsdb:
            os.environ['MY_FSDB_DUMP']="on"
        if self.args.wavetcl==None:
            Simulation_CMD.append('-ucli -do %s'%self.testdb[GroupName]['test'][TestName]['tcl'])
        else:
            Simulation_CMD.append('-ucli -do ${VERIFY_HOME}/%s'%self.args.wavetcl)
        SimulationCMD=" \\\n".join(Simulation_CMD)
        self.PrintLog("%s"%SimulationCMD,True)
        os.chdir("%s"%SimDir)
        result = subprocess.run(SimulationCMD, shell=True, capture_output=True, text=True, timeout=7200)
        if result.returncode != 0:
            self.PrintLog("[WARN] Simulation exited with code %d" % result.returncode, True)

        if self.args.wavetcl==None:
            self.base_simulation_opt.append('-ucli -do %s'%self.testdb[GroupName]['test'][TestName]['tcl'])
        else:
            self.base_simulation_opt.append('-ucli -do ${VERIFY_HOME}/%s'%self.args.wavetcl)
        self.WriteCfgFile(SimDir,CompSim="sim")

# *****************************************************************************************
    def GetBaseCompileOpt(self):
        self.PrintLog("[xrun]:GetBaseCompileOpt",self.PrintEnable)
        self.base_compile_opt=[]
        comp_base_file="%s/comp_base.cfg"%self.cfg_home
        if not os.path.isfile(comp_base_file):
            self.base_compile_opt.append('-full64')
            self.base_compile_opt.append('-l compile.log')
            self.base_compile_opt.append('-sverilog')
            self.base_compile_opt.append('+v2k')
            self.base_compile_opt.append('+evalorder')
            self.base_compile_opt.append('+vcs+lic+wait')
            self.base_compile_opt.append('+libext+.sv+.v+V+.vp+vlib')
            self.base_compile_opt.append('+systemverilogext+.svh')
            self.base_compile_opt.append('+ntb_opts uvm-1.2')
            self.base_compile_opt.append('+lint=TFIPC-L +lint=PCWM')
            self.base_compile_opt.append('-timescale=1ns/1ps')
            self.base_compile_opt.append('-reportstats')
            self.base_compile_opt.append('-j4 -kdb -lca')
            self.base_compile_opt.append('-debug_all')
            self.base_compile_opt.append('+Marchive=1000')
            self.base_compile_opt.append('+notimingcheck')
            self.base_compile_opt.append('+nospecify')
            self.base_compile_opt.append('-top tb_top')
            self.base_compile_opt.append('+define+SYNOPSYS_SV+NTB')
            self.base_compile_opt.append('+define+notiming')
            self.base_compile_opt.append('-P ${VERIFY_HOME}/share/PLI/VCS/LINUX64/novas.tab ${VERIFY_HOME}/share/PLI/VCS/LINUX64/pli.a')
            self.base_compile_opt.append('+warn=noIAVCVF-W')
            self.base_compile_opt.append('+warn=noDRTZ')
            self.base_compile_opt.append('+incdir+${VCS_HOME}/etc/uvm-1.2')
        else:
            self.ReadCfgFile(comp_base_file,CompSim="comp")

        if self.args.cov:
            if not os.path.isfile("%s/coverage.cfg"%self.cfg_home):
                self.base_compile_opt.append('-cm line+cond+fsm+tgl+branch+assert')
            else:
                self.ReadCfgFile("%s/coverage.cfg"%self.cfg_home,CompSim="comp")
        
        if self.args.compcfg!=None:
            self.ReadCfgFile("%s/%s"%(self.tb_home,self.args.compcfg),CompSim="comp")


    def GetBaseSimulationOpt(self):
        self.PrintLog("[xrun]:GetBaseSimulationOpt",self.PrintEnable)
        self.base_simulation_opt=[]
        sim_base_file="%s/sim_base.cfg"%self.cfg_home
        if not os.path.isfile(sim_base_file):
            self.base_simulation_opt.append('-l sim.log')
            self.base_simulation_opt.append('+UVM_VERBOSITY=UVM_MEDIUM')
            self.base_simulation_opt.append('+UVM_TIMEOUT="100000000ps,YES"')
            self.base_simulation_opt.append('+fsdb+all')
            self.base_simulation_opt.append('+vcs+ignorestop')
            self.base_simulation_opt.append('+vcs+loopreport+2')
            self.base_simulation_opt.append('+vcs+loopdetect')
            self.base_simulation_opt.append('-reportstats')
            self.base_simulation_opt.append('+RANDOM_SEED=1 +ntb_random_seed=1')
            if self.args.wavetcl==None:
                self.base_simulation_opt.append('-ucli -do ${VERIFY_HOME}/tcl/wave.tcl')
        else:
            self.ReadCfgFile(sim_base_file,CompSim="sim")

        if self.args.cov:
            if not os.path.isfile("%s/coverage.cfg"%self.cfg_home):
                self.base_simulation_opt.append('-cm line+cond+fsm+tgl+branch+assert')
            else:
                self.ReadCfgFile("%s/coverage.cfg"%self.cfg_home,CompSim="sim")
        
        if self.args.simcfg!=None:
            self.ReadCfgFile("%s/%s"%(self.tb_home,self.args.simcfg),CompSim="sim")

# *****************************************************************************************
    def CheckSimLog(self,CompDir,SimDir,TestName,SEED):
        """检查仿真日志: PASS/FAIL/EXCEPTION"""
        logfile = "%s/sim.log" % SimDir
        
        if not os.path.isfile(logfile):
            self.resultlog += "\n" + ("%s %s \033[31;1m EXCEPTION (no log) \033[0m" % (TestName, SEED))
            self.regressionlog += "\n" + ("%s %s EXCEPTION (no log)" % (TestName, SEED))
            return
        
        with open(logfile, "r") as f:
            log_content = f.read()
        
        # UVM 同时有 "PASSED" 和 "FAILED" 是正常的（多个 sequence 并行时）
        # 判断逻辑: 有 UVM_FATAL → FAIL; 有 UVM_ERROR → FAIL;
        #           仅有 UVM_WARNING 或纯 PASSED → PASS
        has_fatal   = "UVM_FATAL" in log_content
        has_error   = "UVM_ERROR" in log_content
        has_passed  = "UVM TEST PASSED" in log_content
        has_failed  = "UVM TEST FAILED" in log_content
        has_timeout = "UVM TIMEOUT" in log_content
        has_exit    = ("$finish" in log_content and not has_passed and not has_failed)
        
        status = "PASS"
        reason = ""
        
        if has_timeout:
            status = "FAIL"; reason = "TIMEOUT"
        elif has_fatal:
            status = "FAIL"; reason = "FATAL"
        elif has_error:
            status = "FAIL"; reason = "ERROR"
        elif has_failed and not has_passed:
            status = "FAIL"; reason = "FAILED"
        elif has_passed:
            status = "PASS"
        elif has_exit:
            status = "EXCEPTION"; reason = "no PASS/FAIL"
        else:
            status = "EXCEPTION"; reason = "incomplete log"
        
        color = "\033[32;1m" if status == "PASS" else "\033[31;1m"
        self.resultlog += "\n" + ("%s %s %s%s (%s)\033[0m" % (TestName, SEED, color, status, reason))
        self.regressionlog += "\n" + ("%s %s %s (%s)" % (TestName, SEED, status, reason))


    def PrintResultLog(self,CompDir):
        regression_file="%s/../regression"%CompDir
        if not os.path.isfile(regression_file):
            f=open(regression_file,"w+")
            f.write("")
            f.close()
        
        with open(regression_file,'a') as f:
            f.writelines(self.regressionlog)
        
        Title="""
************************************************************
**     Regression Result Log                              **
************************************************************"""
        self.PrintLog("%s\n%s"%(Title,self.resultlog),True)

    def OpenSimLog(self):
        Simualtion_file="./sim.log"
        # no -t
        if self.args.testlib==None:
            raise Exception("Please give the testname!!!")
        
        # no -g and -t
        elif self.args.grouplib==None and self.args.testlib!=None:
            if self.args.seed==None:
                raise Exception("Please give the seed number!!!")
            else:
                Simualtion_file="%s/%s/sim/%s/sim.log"%(self.build_home,self.args.testlib[0],self.args.seed)
                self.PrintLog(Simualtion_file,True)
        
        # -g and -t
        elif self.args.grouplib!=None and self.args.testlib!=None:
            if self.args.seed==None:
                raise Exception("Please give the seed number!!!")
            else:
                Simualtion_file="%s/%s/sim/%s/%s/sim.log"%(self.build_home,self.grouplib[0],self.args.testlib[0],self.args.seed)
                self.PrintLog(Simualtion_file,True)
        subprocess.Popen(["open","-a","TextEdit",Simualtion_file])

    def CreateCoverageDir(self,GroupName,TestName):
        self.PrintLog("[xrun]:CreateCoverageDir",self.PrintEnable)
        #self.CreateDir("%s"%self.coverage_home)
        os.chdir(self.coverage_home)
        self.CreateDir("%s"%self.coverage_result_dir)
        os.chdir(self.coverage_result_dir)
        # no -g and no -t
        if GroupName==None and TestName==None:
            raise Exception("Give at least one grouname or testname!!!")
        # -g and -t
        elif GroupName!=None and TestName!=None:
            self.CreateDir("%s"%GroupName[0])
        # -g and no -t
        elif GroupName!=None and TestName==None:
            self.CreateDir("%s"%GroupName[0])
        # no -g and -t
        elif GroupName==None and TestName!=None:
            groupname=self.MatchGroupAccordingToCase(TestName[0])
            self.CreateDir("%s"%groupname)

    def MergeCoverage(self):
        self.PrintLog("[xrun]:MergeCoverage",self.PrintEnable)
        #merge coverage of group's case.vdb
        vdb_dir=[]
        vdb_dir=self.GetDirName(self.coverage_result_dir,'.vdb')
        if vdb_dir=="":
            raise Exception("There is no vdbdir of coverage,Please ensure whether you had done right!!!")
        for i in range(len(vdb_dir)):
            vdb_file=[]
            vdb_file=self.GetFileName("%s/%s"%(self.coverage_result_dir,vdb_dir[i]),'.vdb')
            if vdb_file=="":
                raise Exception("There is no vdbfile of coverage,Please ensure whether you had done right!!!")

            Merge_CMD=[]
            Merge_CMD.append("urg -full64")
            for j in range(len(vdb_file)):
                Merge_CMD.append("-dir %s/%s/%s"%(self.coverage_result_dir,vdb_dir[i],vdb_file[j]))
            Merge_CMD.append("-dbname %s/%s.vdb"%(self.coverage_result_dir,vdb_dir[i]))
            MergeCMD=" \\\n".join(Merge_CMD)
            self.PrintLog(MergeCMD,True)
            subprocess.run(MergeCMD, shell=True, check=True, capture_output=True, text=True)

    def OpenCoverage(self):
        self.PrintLog("[xrun]:OpenCoverage",self.PrintEnable)
        OpenCov_CMD="verdi -cov -covdir %s&"%self.args.opencov
        subprocess.Popen(OpenCov_CMD, shell=True)

# *****************************************************************************************

    def CreateDir(self,DirName):
        if not os.path.isdir(DirName):
            os.mkdir(DirName)
        else:
            self.PrintLog("The dir is exist already!",self.PrintEnable)

    def SeedGen(self):
        if self.args.seed:
            seed=self.args.seed
        else:
            seed=random.randint(0,2**16)
        return seed

    def MatchGroupAccordingToCase(self,TestName):
        groupname=[]
        for group in self.testgroup:
            gg=group.split("/")[-1]
            for case in self.testdb[gg]['test'].keys():
                if case==TestName:
                    groupname=gg
        return groupname

    def ReadCfgFile(self,FilePath,CompSim):
        with open("%s"%FilePath,'r') as f:
            lines=f.readlines()
            for i in range(len(lines)):
                if CompSim=="comp":
                    if lines[i].strip("\n")[:2]!="//" and lines[i].strip("\n")[:1]!="#":
                        self.base_compile_opt.append(lines[i].strip("\n"))

                if CompSim=="sim":
                    if lines[i].strip("\n")[:2]!="//" and lines[i].strip("\n")[:1]!="#":
                        self.base_simulation_opt.append(lines[i].strip("\n"))
    
    def WriteCfgFile(self,FilePath,CompSim):
        if CompSim=="comp":
            f=open("%s/compile.opt"%FilePath,"w+")
            for i in range(len(self.base_compile_opt)):
                f.write("%s\n"%self.base_compile_opt[i])
            f.close()

        if CompSim=="sim":
            f=open("%s/simulation.opt"%FilePath,"w+")
            for i in range(len(self.base_simulation_opt)):
                f.write("%s\n"%self.base_simulation_opt[i])
            f.close()    

    def GetDirName(self,Path,Suffix):
        dir_name=[]
        flist=os.listdir(Path)
        for i in flist:
            if not os.path.splitext(i)[1]==Suffix:
                dir_name.append(i)
        return dir_name
    
    def GetFileName(self,Path,Suffix):
        file_name=[]
        flist=os.listdir(Path)
        for i in flist:
            if os.path.splitext(i)[1]==Suffix:
                file_name.append(i)
        return file_name
    
    def SimvFileExist(self,Path):
        if os.path.isfile("%s/simv"%Path):
            self.PrintLog("The compilation has already been executed and does not need to be re-executed!!!")
            exit()
    
    def PrintLog(self,StrStr,PrintEnable):
        if PrintEnable==True:
            print("%s"%StrStr)

    def PrintArray(self,Array,PrintEnable):
        if PrintEnable==True:
            for i in range(len(Array)):
                print(Array[i])

# *****************************************************************************************
    def ReadKfile(self,Dir,CfgFile,CompileDir):
        self.PrintLog("[xrun]:ReadKfile",self.PrintEnable)
        rtl_kfile   ="%s/rtl.k" %self.filelist_home
        tb_kfile    ="%s/tb.k"  %self.filelist_home
        vip_kfile   ="%s/vip.k" %self.filelist_home
        cmodel_kfile="%s/cmodel.k" %self.filelist_home

        rtl_newfile ="%s/rtl_new.f" %CompileDir
        tb_newfile  ="%s/tb_new.f"  %CompileDir
        vip_newfile ="%s/vip_new.f" %CompileDir
        cmodel_newfile ="%s/cmodel_new.f" %CompileDir

        #rtl
        if not os.path.isfile(rtl_kfile):
            self.rtlkfile=False
        else:
            self.rtlkfile=True
            self.gen_kf_ff_info(rtl_kfile,rtl_newfile,CfgFile,self.PrintEnable)
        #tb
        if not os.path.isfile(tb_kfile):
            self.tbkfile=False
        else:
            self.tbkfile=True
            self.gen_kf_ff_info(tb_kfile,tb_newfile,CfgFile,self.PrintEnable)
        #vip
        if not os.path.isfile(vip_kfile):
            self.vipkfile=False
        else:
            self.vipkfile=True
            self.gen_kf_ff_info(vip_kfile,vip_newfile,CfgFile,self.PrintEnable)    
        #cmodel
        if not os.path.isfile(cmodel_kfile):
            self.cmodelkfile=False
        else:
            self.cmodelkfile=True
            self.gen_kf_ff_info(cmodel_kfile,cmodel_newfile,CfgFile,self.PrintEnable)  

    def GetDefineInfo(self,FilePath):
        self.PrintLog("[xrun]:GetDefineInfo",self.PrintEnable)
        kfileToffile_define=[]
        if os.path.isfile(FilePath):
            lines=open(FilePath,"r").read()
            result=""
            kfileToffile_define=re.findall(r"[+]define[+](.*?)\n",lines)
            result=result+'\n'.join(kfileToffile_define)
        else:
            self.PrintLog("The Path of %s is not exist!!!"%FilePath,True)
    
    def gen_kf_ff_info(self,FilePath,NewFilePath,CfgFile,PrintEnable):
        """展开 .k 文件中的 `ifdef/`else/`endif，输出到 _new.f"""
        Enable=PrintEnable
        if not os.path.isfile(FilePath):
            self.PrintLog("[WARN] K-file not found: %s" % FilePath, True)
            return
        
        with open(FilePath,'r') as f:
            lines = f.readlines()
        
        DefineInfo = self.GetDefineInfo(CfgFile)
        define_set = set(DefineInfo) if DefineInfo else set()
        self.PrintLog("[KFile] defines: %s" % define_set, Enable)
        
        # 栈式 ifdef 展开：每个栈帧记录 {active, had_true_branch}
        stack = [{"active": True, "had_true": False}]
        result = []
        
        for line in lines:
            s = line.strip()
            
            # 检测 `ifdef MACRO
            m = re.match(r'`ifdef\s+(\S+)', s)
            if m:
                macro = m.group(1)
                is_defined = macro in define_set
                frame = stack[-1]
                new_active = frame["active"] and is_defined
                stack.append({
                    "active": new_active,
                    "had_true": new_active,
                    "macro": macro,
                })
                result.append("")  # 指令行不输出
                continue
            
            # 检测 `else
            if s.startswith('`else'):
                frame = stack[-1]
                # 翻转: 如果之前是active且已命中→变false; 否则如果父级active且未命中→变true
                if frame["had_true"]:
                    frame["active"] = False
                else:
                    parent = stack[-2] if len(stack)>=2 else {"active": True}
                    frame["active"] = parent["active"] and not frame["had_true"]
                result.append("")
                continue
            
            # 检测 `endif
            if s.startswith('`endif'):
                if len(stack) > 1:
                    stack.pop()
                result.append("")
                continue
            
            # 普通行: 当前栈顶 active → 输出
            if stack[-1]["active"]:
                result.append(line)
            else:
                result.append("")
        
        # 写入新文件
        with open(NewFilePath, 'w') as f:
            for line in result:
                if line:
                    f.write(line.lstrip())
        
        # 报告
        total = len(lines)
        kept = sum(1 for r in result if r.strip())
        self.PrintLog("[KFile] %s: %d/%d lines kept after ifdef expansion" % (FilePath, kept, total), Enable)

