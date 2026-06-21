#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from common_lib.parameters import Parameters

class gen_sourceme:

    def __init__(self):
        local_dir='./'
        print("[gen_sourceme]:initiail")
        self.gen_sourceme_file(local_dir,PrintEnable=True)

    def gen_sourceme_file(self,local_dir,PrintEnable):
        os.chdir(local_dir)
        filename = open("SourceMe", "w+")
        filename.write("#! /usr/env bash\n")
        filename.write("##=======================\t[Cmodel Tools]\t=======================##\n")
        filename.write("##=======================\t[EDA env setting]\t====================##\n")
        filename.write("#VCS/VERDI tools\n")
        filename.write("export TOOLS_PATH=/network/tools/synopsys\n")
        filename.write("export VCS_HOME=${TOOLS_PATH}/vcs_mx/vcs_mx_vN-2017.12-SP2\n")
        filename.write("export VERDI_HOME=${TOOLS_PATH}/verdi/verdi_vN-2017.12-SP2\n")
        filename.write("export LD_LIBRARY_PATH=${VERDI_HOME}/share/PLI/lib/LINUX64:${LD_LIBRARY_PATH}\n")
        filename.write("#export LD_LIBRARY_PATH=${VERDI_HOME}/share/PLI/lib/LINUXAMD64:${LD_LIBRARY_PATH}\n")
        filename.write("export LM_LICENSE_FILE=27020@192.168.1.50:27000:@eda51\n")
        filename.write("export CDS_LIC_FILE=5280@eda93\n")
        filename.write("export DW_FILE_PATH=\"${TOOLS_PATH}/syn_vM-2016.12-SP3.old\"\n")
        filename.write("#export LEDA_PATH=${TOOLS_PATH}/G-2012.09\n")
        filename.write("export PATH=$PATH:$VCS_HOME/bin:$VERDI_HOME/bin\n")
        filename.write("#export PS1=\"[\\u@\\h \\w]\"\n")
        filename.write("export PS1=\"[\\u@\\h \\W]$\"\n")
        filename.write("#VIP\n")
        filename.write("export DESIGNWARE_HOME=/networkpub/project/VIP/synopsys\n")
        filename.write("export LIB_PATH=/network/project/public/uvm_vip\n")
        filename.write("#export VIP_APB_DIR=${LIB_PATH}/apb_lib\n")
        filename.write("#export VIP_AHB_DIR=${LIB_PATH}/ahb_lib\n")
        filename.write("#export VIP_AXI_DIR=${LIB_PATH}/axi_lib\n")
        filename.write("##=======================\t[RTL/TB path setting]\t=================##\n")
        filename.write("export VERIFY_HOME=$PWD\n")
        filename.write("export NPU_PRJ_PATH=${VERIFY_HOME}/../../..\n")
        filename.write("export RTL_HOME=${PRJ_HOME}/rtl\n")
        filename.write("export TESTPLAN_HOME=${VERIFY_HOME}/testplan\n")
        filename.write("export JSON_HOME=${VERIFY_HOME}/json\n")
        filename.write("export TOOLS_HOME=${VERIFY_HOME}/run\n")
        filename.write("export PATH=$PATH:$JSON_HOME\n")
        filename.write("export PATH=$PATH:$TOOLS_HOME\n")
        filename.write("export TEST_PARALLEL_NUM=8\n")
        filename.write("#export MY_FSDB_DUMP=on\n")
        filename.write("export EMAIL_SUBJECT=\"XX UT/IT VERIFY REGRESSION\"\n")
        filename.write("export EMAIL_RECEIVES=\"wangxinxin@dev.com\"\n")
        filename.write("# add the xx.so of yourself\n")
        filename.write("#export LD_LIBRARY_PATH=${VERIFY_HOME}/reference/xx/3rd_path/systemc/lib64:${LD_LIBRARY_PATH}\n")
        filename.write("##=======================\t[compile setting]\t===========##\n")
        if Parameters.TopCoreArch!=None:
            filename.write("##Top Core %s Tools\n"                      %Parameters.TopCoreArch.upper())
            filename.write("# export %s_TOOLS=${VERIFY_HOME}/../..\n"   %Parameters.TopCoreArch.upper())
            filename.write("# export PATH=$PATH:%s_TOOLS\n"             %Parameters.TopCoreArch.upper())
        if Parameters.SubCoreArch!=None:
            filename.write("##Sub Core %s Tools\n"                      %Parameters.SubCoreArch.upper())
            filename.write("# export %s_TOOLS=${VERIFY_HOME}/../..\n"   %Parameters.SubCoreArch.upper())
            filename.write("# export PATH=$PATH:%s_TOOLS\n"             %Parameters.SubCoreArch.upper())
        filename.write("##=======================\t[Your's Alias]\t=======================##\n")
        filename.write("alias cdrtl=\"cd ${RTL_HOME}\"\n")
        filename.write("#alias cdut=\"cd ${VERIFY_HOME}\"\n")
        filename.write("#alias cdit=\"cd ${VERIFY_HOME}\"\n")
        filename.write("#alias cdst=\"cd ${VERIFY_HOME}\"\n")
        filename.write("#alias openvpd=\"dve -full64 sim.vpd&\"\n")
        filename.write("#alias openfsdb=\"verdi -ssf sim.fsdb&\"\n")
        filename.write("alias openvpd=\"bsub -Is -q rca.q dve -full64 sim.vpd&\"\n")
        filename.write("alias openfsdb=\"bsub -Is -q rca.q verdi -ssf sim.fsdb&\"\n")
        filename.write("alias showcoverage_dve=\"dve -full64 -cov -dir cov_merge.vdb&\"\n")
        filename.write("alias showcoverage_verdi=\"verdi -cov -covdir cov_merge.vdb&\"\n")
        filename.write("echo \"Bootenv Finish\"\n")
        filename.close()

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")

if __name__ == '__main__':
    #local_dir='./'
    gen=gen_sourceme()