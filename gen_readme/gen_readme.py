#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from common_lib.parameters import Parameters

class gen_readme:

    def __init__(self):
        local_dir='./'
        print("[gen_readme]:initiail")
        #self.local_dir = os.getcwd()
        self.gen_readme_file(local_dir)

    def gen_readme_file(self,local_dir):
        os.chdir(local_dir)
        print('[readme]:'+local_dir)
        #filename = open("readme", "w+")
        filename = open(Parameters.readme, "w+")
        filename.write("//the operation of flow\n")
        filename.write("\n")
        filename.write("1: the flow/cmd of running case\n")
        filename.write("\t(1) \"source sourceme\"                                       //Setting environment variables\n")
        filename.write("\t(2) \"run/xrun -l\"                                           //Displays the current case list\n")
        filename.write("\t(3) \"run/xrun -g casegroup -t case -c\"                      //compile the case\n")
        filename.write("\t(4) \"run/xrun -g casegroup -t case -s\"                      //Simulate the case\n")
        filename.write("\t(5) \"run/xrun -g casegroup -t case -s --fsdb\"               //Simulate the case,with fsdb,random seed\n")
        filename.write("\t(6) \"run/xrun -g casegroup -t case -s --fsdb --seed=1\"      //Simulate the case,with fsdb,specific seed 1\n")
        filename.write("\t(7) \"run/xrun -g casegroup -t case -s --fsdb -n 10\"         //Simulate the case,with fsdb,random seed,repeat 10\n")
        filename.write("\n")
        filename.write("2: the cmd/flow of regression case\n")
        filename.write("\t(1) \"run/xrun -g casegroup -c\"                              //compile the all case of group \n")
        filename.write("\t(2) \"run/xrun -g casegroup -s\"                              //Simulate the all case of group,without fsdb,random seed\n")
        filename.write("\t(3) \"run/xrun -g casegroup -s -m\"                           //Simulate the all case of group,without fsdb,random seed,email results\n")
        filename.write("\n")
        filename.write("3: the cmd/flow of coverage\n")
        filename.write("\t(1) \"run/xrun -g casegroup -c --cov\"                        //compile the all case of group,with coverage\n")
        filename.write("\t(2) \"run/xrun -g casegroup -s --cov\"                        //Simulate the all case of group,without fsdb,random seed,with coverage\n")
        filename.write("\t(3) \"run/xrun -g casegroup -s --cov -n 10\"                  //Simulate the all case of group,without fsdb,random seed,repeat 10,with coverage\n")
        filename.write("\t(4) \"xrun --covmerge\"                                       //merge the all coverage\n")
        filename.write("\t(4) \"xrun --opencov\"                                        //open the coverage after merge\n")
        filename.write("\n")
        filename.write("4: the cmd of hellp\n")
        filename.write("\t(1) \"run/xrun -h\"                                           //Displays the detailed command function\n")
        filename.write("\n")
        filename.write("===========================================================================================================\n")
        filename.write("NOTE:\n")
        filename.write("    Before running the environment for the first time, you may need to convert the following three files to unix format:\n")
        filename.write("    gvim After opening the file, run \"set ff=unix\" on the command line\n")
        filename.write("    (1)run/xrun\n")
        filename.write("    (2)cfg/comp_base.cfg\n")
        filename.write("    (3)cfg/sim_base.cfg\n")
        filename.write("    (4)cfg/xx.cfg\n")
        filename.close()

if __name__ == '__main__':
    #local_dir='./'
    gen=gen_readme()