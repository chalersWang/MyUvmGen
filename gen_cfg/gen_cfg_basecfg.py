#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import sys
sys.path.append(r".\..") 

from common_lib.parameters import Parameters

class gen_cfg_basecfg:

    def __init__(self):
        print("[gen_cfg_basecfg]:initiail")
        PrintEnable=True
        self.gen_cfg_basecfg_info(PrintEnable)

    def gen_cfg_basecfg_info(self,PrintEnable):
        #================================================================================
        #filename = open("comp_base.cfg", "w+")
        filename = open(Parameters.Cfg_comp_base_file, "w+")
        filename.write("-full64                                 \n")
        filename.write("-l compile.log                          \n")
        filename.write("-sverilog                               \n")
        filename.write("+v2k                                    \n")
        filename.write("+evalorder                              \n")
        filename.write("+vcs+lic+wait                           \n")
        filename.write("+libext+.sv+.v+V+.vp+vlib               \n")
        filename.write("+systemverilogext+.svh                  \n")
        filename.write("-ntb_opts uvm-1.2                       \n")
        filename.write("+lint=TFIPC-L +lint=PCWM                \n")
        filename.write("-timescale=1ns/1ps                      \n")
        filename.write("//-override_timescale                   \n")
        filename.write("-reportstats                            \n")
        filename.write("-j4 -kdb -lca                           \n")
        filename.write("-debug_all                              \n")
        filename.write("+Marchive=1000                          \n")
        filename.write("+notimingcheck                          \n")
        filename.write("+nospecify                              \n")
        filename.write("-top tb_top                             \n")
        filename.write("+vcs+initreg+random                     \n")
        filename.write("+define+SYNOPSYS_SV+NTB                 \n")
        filename.write("+define+notiming                        \n")
        filename.write("//+UVM_CB_TRACE_ON                      \n")
        filename.write("-P ${VERDI_HOME}/share/PLI/VCS/LINUX64/novas.tab ${VERDI_HOME}/share/PLI/VCS/LINUX64/pli.a\n")
        filename.write("//+warn=[no]ID|none|all,...             \n")
        filename.write("+warn=noIAVCVF-W                        \n")
        filename.write("+warn=noDRTZ                            \n")
        filename.write("+incdir+${VCS_HOME}/etc/uvm-1.2         \n")
        filename.write("//-file ${VERIFY_HOME}/cfg/%s           \n"%Parameters.Cfg_debug_file)
        filename.write("//-file ${VERIFY_HOME}/cfg/%s           \n"%Parameters.Cfg_coverage_file)
        filename.write("//-file ${VERIFY_HOME}/cfg/%s           \n"%Parameters.Cfg_assertion_file)
        filename.write("//-xprop=${VERIFY_HOME}/cfg/%s          \n"%Parameters.Cfg_xprop_file)
        filename.write("//-report=xprop                         \n")
        filename.write("//-partcomp\n")
        filename.write("//-partcomp=autopart_low\n")
        filename.write("//-partcomp=autopart_medium\n")
        filename.write("//-partcomp=autopart_high\n")
        filename.write("//-partcomp -topcfg %s\n"%Parameters.Cfg_partitioncomp_file)
        filename.write("//-pcmakeprof                           \n")
        filename.close()

        #================================================================================
        filename = open(Parameters.Cfg_sim_base_file, "w+")
        filename.write("-l sim.log                              \n")
        filename.write("+UVM_VERBOSITY=UVM_MEDIUM               \n")
        filename.write("+UVM_TIMEOUT=\"1000000000ps,YES\"       \n")
        filename.write("+fsdb+all                               \n")
        filename.write("+vcs+ignorestop                         \n")
        filename.write("+vcs+loopreport+2                       \n")
        filename.write("+vcs+loopdetect                         \n")
        filename.write("+vcs+initreg+random                     \n")
        filename.write("//+vcs+initreg+0|1|x|z                  \n")
        filename.write("//+vcs+initmem+0|1|x|z                  \n")
        filename.write("-reportstats                            \n")
        filename.write("+RANDOM_SEED=1 +ntb_random_seed=1       \n")
        filename.write("//+simprofile                           \n")
        filename.write("//+UVM_VERDI_TRACE=\"UVM_AWARE+HIER\"   \n")
        # filename.write("//+UVM_DUMP_CMDLINE_ARGS                \n")
        # filename.write("//+UVM_CONFIG_DB_TRACE                  \n")
        # filename.write("//+UVM_PHASE_TRACE                      \n")
        # filename.write("//+UVM_OBJECTION_TRACE                  \n")
        # filename.write("//-file ${VERIFY_HOME}/cfg/%s           \n"%Parameters.Cfg_debug_file)
        filename.write("//-ucli -do ${VERIFY_HOME}/tcl/wave.tcl \n")
        filename.write("//-file {VERIFY_HOME}/cfg/%s            \n"%Parameters.Cfg_coverage_file)
        filename.write("//-file {VERIFY_HOME}/cfg/%s            \n"%Parameters.Cfg_assertion_file)
        filename.write("//-xprop={VERIFY_HOME}/cfg/%s           \n"%Parameters.Cfg_xprop_file)
        filename.write("//-report=xprop                         \n")
        filename.close()

        #================================================================================
        filename = open(Parameters.Cfg_debug_file, "w+")
        filename.write("//For details about how to debug, see:                          \n")
        filename.write("//<1>https://www.elecfans.com/d/2051737.html                    \n")
        filename.write("//<2>https://www.cnblogs.com/Alfred-HOO/articles/17510025.html  \n")
        filename.write("-gui=verdi                                                      \n")
        filename.write("+UVM_VERDI_TRACE=\"UVM_AWARE+RAL+HIER+COMPWAVE\"\n")
        filename.write("+UVM_TR_RECORD                                  \n")
        filename.write("+UVM_LOG_RECORD                                 \n")
        filename.write("+UVM_DUMP_CMDLINE_ARGS                          \n")
        filename.write("+UVM_CONFIG_DB_TRACE                            \n")
        filename.write("+UVM_RESOURCE_DB_TRACE                          \n")
        filename.write("+UVM_PHASE_TRACE                                \n")
        filename.write("+UVM_OBJECTION_TRACE                            \n")
        filename.write("+define+UVM_CB_TRACE_ON                         \n")
        filename.close()

        filename = open(Parameters.Cfg_xprop_file, "w+")
        filename.write("//tree      {tb_top}        {xpropOn}   \n")
        filename.write("//module    {module}        {xpropOff}  \n")
        filename.write("//instance  {instance}      {xpropOff}  \n")
        filename.write("merge=xmerge                            \n")
        filename.close()

        filename = open(Parameters.Cfg_coverage_file, "w+")
        filename.write("-cm line+cond+fsm+tgl+branch+assert     \n")
        filename.write("-cm_line contassign                     \n")
        filename.write("//-cm_cond allops                       \n")
        filename.write("//-cm_hier ${VERIFY_HOME}/coverage/code/CoverageHierarchy.lst \n")
        filename.write("//-file ${VERIFY_HOME}/coverage/code/CoverageDefine.lst \n")
        filename.close()

        filename = open(Parameters.Cfg_assertion_file, "w+")
        filename.write("//-assert_hier=AssertionHierarchy.lst    \n")
        filename.write("//AssertionHierarchy.lst: -tree tb_top.DUT.xx.* \n")
        filename.close()

        filename = open(Parameters.Cfg_partitioncomp_file, "w+")
        filename.write("config topcfg;\n")
        filename.write("    partition instance  top_tb.DUT;\n")
        filename.write("    partition cell      module_name;\n")
        filename.write("    partition package   uvm_pkg;\n")
        filename.write("    partition package   svt_xx_uvm_pkg;\n")
        filename.write("    partition package   xx_UvcTop;\n")
        filename.write("    partition package   xx_EnvTop;\n")
        filename.write("    partition package   xx_TestTop;\n")
        filename.write("endconfig\n")
        filename.close()

        #================================================================================
        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")
            # newlines=[]
            # with open('base.cfg','r',encoding='utf-8') as f:
            #     lines=f.readlines()
            #     for j in range(len(lines)):
            #         if lines[j] == '},}':
            #             newlines.append("}}")
            #         else:
            #             newlines.append(lines[j])

            # for i in range(len(newlines)):
            #     print(newlines[i].replace('\n',''))

if __name__ == '__main__':
    gen=gen_cfg_basecfg()