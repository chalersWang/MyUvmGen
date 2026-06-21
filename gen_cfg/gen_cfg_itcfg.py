#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-

class gen_cfg_itcfg:

    def __init__(self):
        print("[gen_cfg_itcfg]:initial")
        PrintEnable=True
        self.gen_cfg_itcfg_info(PrintEnable)

    def gen_cfg_itcfg_info(self,PrintEnable):
        filename = open("it.cfg", "w+")
        filename.write("-full64                            \n")
        filename.write("-partcomp -Mupdate                 \n")
        filename.write("-top tb_top                        \n")
        filename.write("-l comp.log                        \n")
        filename.write("-sverilog                          \n")
        filename.write("-+v2k                              \n")
        filename.write("+evalorder                         \n")
        filename.write("+vcs+lic+wait                      \n")
        filename.write("+systemverilogext.svh              \n")
        filename.write("+libext+.sv+.v+.V+.vp.vlib         \n")
        filename.write("+vc -lca -j4                       \n")
        filename.write("-ntb_opts uvm-1.2                  \n")
        filename.write("+lint=TFIPC +lint=PCWM             \n")
        filename.write("-timescale=1ns/1ps                 \n")
        filename.write("+debug_all                         \n")
        filename.write("-Marchive=2000                     \n")
        filename.write("+define+no_timing                  \n")
        filename.write("+notimingcheck                     \n")
        filename.write("+nospecify                         \n")
        filename.write("-reportstats                       \n")
        filename.write("-error=noMPD                       \n")
        filename.write("+define+DUMP_FSDB_FILE             \n")
        filename.write("-P ${VERDI_HOME}/share/PLI/VCS/LINUX64/novas.tab  ${VERDI_HOME}/share/PLI/VCS/LINUX64/pli.a    \n")
        filename.write("+incdir+${VCS_HOME}/etc/uvm-1.2   \n")
        #filename.write("-file ${RTL_FILELIST}             \n")
        #filename.write("-file ${VIP_FILELIST}             \n")
        #filename.write("-file ${C_FILELIST}               \n")
        #filename.write("-file ${TB_FILELIST}              \n")
        filename.write("+UVM_TIMEOUT=\"100000000ps,YES\"  \n")
        filename.write("+UVM_VERBOSITY=UVM_MEDIUM         \n")
        #filename.write("-sv_lib libdpi                    \n")
        filename.write("+vcs+ignorestop                   \n")
        filename.write("+vcs+loopdetect +vcs+loopreport+2 \n")
        filename.write("-ucli -do ${VERIFY_HOME}/tcl/wave.tcl    \n")
        filename.close()

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")
            with open('it.cfg','r',encoding='utf-8') as f:
                lines=f.readlines()
            for i in range(len(lines)):
                print(lines[i].replace('\n',''))

if __name__ == '__main__':
    gen=gen_cfg_itcfg()