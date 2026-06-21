#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from readexcel.readexcel_WorkingDirectoryGen import readexcel_WorkingDirectoryGen
from common_lib.parameters import Parameters

class gen_tb_dumpctrl:

    def __init__(self):
        print("[gen_tb_dumpctrl]:initial")
        #EnvironmentGenCfg='../VerifyEnvironmentGenCfg.xlsx'
        EnvironmentGenCfg=Parameters.EnvironmentGenCfg
        readexcel_WorkingDirectoryGen.readexcel_WorkingDirectoryGen_info(self,EnvironmentGenCfg,PrintEnable=False)
        self.gen_tb_dumpctrl_info(None,PrintEnable=True)

    def gen_tb_dumpctrl_info(self,FileName,PrintEnable):
        if FileName==None:
            filename = open('dumpctrl.sv', "w+")
        else:
            filename=FileName
        
        filename.write("                                                      \n")
        filename.write("///dump vpd file                                      \n")
        filename.write("`ifdef DUMP_VPD_FILE                                  \n")
        filename.write("  reg[1023:0]vpdfile;                                 \n")
        filename.write("  initial                                             \n")
        filename.write("  begin                                               \n")
        filename.write("      if($value$plusargs(\"VPDNAME=%s\",vpdfile))     \n")
        filename.write("          begin                                       \n")
        filename.write("              $vcdplusfile(vpdfile);                  \n")
        filename.write("              $vcdpluson();                           \n")
        filename.write("          end                                         \n")
        filename.write("  end                                                 \n")
        filename.write("`endif                                                \n")
        filename.write("                                                      \n")
        filename.write("///dump fsdb file                                     \n")
        filename.write("`ifdef DUMP_FSDB_FILE                                 \n")
        filename.write("  reg[1023:0]fsdbfile;                                \n")
        filename.write("  initial                                             \n")
        filename.write("  begin                                               \n")
        filename.write("      if($value$plusargs(\"FSDBNAME=%s\",fsdbfile))   \n")
        filename.write("          begin                                       \n")
        filename.write("              /*$fsdbAutoSwitchDumpfile  Format:*/\n")
        filename.write("              /*$fsdbAutoSwitchDumpfile(File_size(MB), File_name, number_of_file)*/\n")
        filename.write("              //$fsdbAutoSwitchDumpfile(2048,fsdbfile,10,\"fsdb.log\");\n")
        filename.write("                                                      \n")
        filename.write("              /*Specify the fsdb file name for the dump waveform*/\n")
        filename.write("              $fsdbDumpfile(fsdbfile);                \n")
        filename.write("                                                      \n")
        filename.write("              /*0 indicates that dump starts from xxx_top for all layers*/\n")
        filename.write("              $fsdbDumpvars(0,tb_top);                \n")
        filename.write("                                                      \n")
        filename.write("              /*dump a two-dimensional array. vcs compile with -debug_all*/\n")
        filename.write("              //$fsdbDumpDMA();                       \n")
        filename.write("                                                      \n")
        filename.write("              /*Start and end dump times. If no start and end times are set,*/\n")
        filename.write("              /*the default dump time is from the start to the end of the simulation*/\n")
        filename.write("              //#0      $fsdbDumpon();                \n")
        filename.write("              //#10000  $fsdbDumpoff();               \n")
        filename.write("          end                                         \n")
        filename.write("  end                                                 \n")
        filename.write("`endif                                                \n")
 
        if FileName==None:
            filename.close()

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")

if __name__ == '__main__':
    gen=gen_tb_dumpctrl()