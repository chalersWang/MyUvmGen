#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os
import operator
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from readexcel.readexcel_DutSignal import readexcel_DutSignal
from readexcel.readexcel_ClockRst import readexcel_ClockRst
from readexcel.readexcel_WorkingDirectoryGen import readexcel_WorkingDirectoryGen
from readexcel.readexcel_VIP import readexcel_VIP
from common_lib.parameters import Parameters

class gen_filelist_file:

    def __init__(self):
        print("[gen_filelist_file]:initial")
        #EnvironmentGenCfg='../VerifyEnvironmentGenCfg.xlsx'
        EnvironmentGenCfg=Parameters.EnvironmentGenCfg
        tb_name=Parameters.tb_name
        DUT_GroupName='example'
        readexcel_WorkingDirectoryGen.readexcel_WorkingDirectoryGen_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_VIP.readexcel_VIP_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_VIP.readexcel_VIP_AXI_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_ClockRst.readexcel_ClockRst_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_DutSignal.readexcel_DutSignal_info(self,EnvironmentGenCfg,PrintEnable=False)
        self.gen_filelist_file_info(tb_name,self.DUT_GroupName,PrintEnable=True)

    def gen_filelist_file_info(self,tb_name,DUT_GroupName,PrintEnable):
        # rtl.f
        #rtl_filename = open("rtl.f", "w+")
        rtl_filename = open(Parameters.Filelist_rtl, "w+")
        rtl_filename.write("//add the filelist of rtl here!!!\n")
        rtl_filename.write("//-f ${VERIFY_HOME}/../../rtl/file.f \n")
        rtl_filename.close()
        # netlist.f
        #netlist_filename = open("netlist.f", "w+")
        netlist_filename = open(Parameters.Filelist_netlist, "w+")
        netlist_filename.write("//add the filelist of netlist here!!!\n")
        netlist_filename.write("//-f ${VERIFY_HOME}/../../netlist/file.f \n")
        netlist_filename.close()
        # tb.f
        #tb_filename = open("tb.f", "w+")
        tb_filename = open(Parameters.Filelist_tb, "w+")
        tb_filename.write("//add the dir of tb here!!!            \n")
        tb_filename.write("+incdir+${VERIFY_HOME}/cfg             \n")
        tb_filename.write("+incdir+${VERIFY_HOME}/tb              \n")
        tb_filename.write("+incdir+${VERIFY_HOME}/env             \n")
        tb_filename.write("+incdir+${VERIFY_HOME}/tb              \n")
        tb_filename.write("+incdir+${VERIFY_HOME}/sva             \n")
        tb_filename.write("+incdir+${VERIFY_HOME}/sva/code        \n")
        tb_filename.write("+incdir+${VERIFY_HOME}/coverage        \n")
        tb_filename.write("+incdir+${VERIFY_HOME}/coverage/code   \n")
        tb_filename.write("+incdir+${VERIFY_HOME}/uvc             \n")
        for i in range(len(DUT_GroupName)):
            # if self.DUT_VIP[i]==False:
            #     tb_filename.write("+incdir+${VERIFY_HOME}/uvc/%s  \n"%DUT_GroupName[i])
            # else:
            #     tb_filename.write("+incdir+${VERIFY_HOME}/uvc/%s  \n"%DUT_GroupName[i].lower())
            tb_filename.write("+incdir+${VERIFY_HOME}/uvc/%s  \n"%DUT_GroupName[i])
            if self.DUT_VIP[i]==True:
                tb_filename.write("+incdir+${VERIFY_HOME}/uvc/%s_vip  \n"%DUT_GroupName[i])

        tb_filename.write("+incdir+${VERIFY_HOME}/reference       \n")
        tb_filename.write("+incdir+${VERIFY_HOME}/regmodel        \n")
        tb_filename.write("+incdir+${VERIFY_HOME}/testcase        \n")
        tb_filename.write("+incdir+${VERIFY_HOME}/testcase/sequence_lib\n")
        tb_filename.write("\n")
        tb_filename.write("${VERIFY_HOME}/sva/%s                  \n"%Parameters.SvaVifDefine)
        tb_filename.write("\n")
        tb_filename.write("//add the .svh of env/uvc/testcase     \n")
        #tb_filename.write("${VERIFY_HOME}/uvc/%s_xx_UvcTop.svh    \n"%(self.tb_name))
        for i in range(len(DUT_GroupName)):
            if self.DUT_VIP[i]==True:
                tb_filename.write("${VERIFY_HOME}/uvc/%s_vip/%s_UvcTop.svh    \n"%(DUT_GroupName[i],DUT_GroupName[i].lower()))
                tb_filename.write("\n")
        for i in range(len(DUT_GroupName)):
            # if self.DUT_VIP[i]==False:
                tb_filename.write("${VERIFY_HOME}/uvc/%s/%s_vif.sv    \n"%(DUT_GroupName[i],DUT_GroupName[i]))
                tb_filename.write("${VERIFY_HOME}/uvc/%s/%s_UvcTop.svh    \n"%(DUT_GroupName[i],DUT_GroupName[i]))
                tb_filename.write("\n")
        tb_filename.write("//add the virtual interface            \n")
        #tb_filename.write("${VERIFY_HOME}/sva/VifMacroDefine.v    \n")
        tb_filename.write("${VERIFY_HOME}/sva/%s_vif.sv           \n"%(tb_name))
        tb_filename.write("                                       \n")
        tb_filename.write("${VERIFY_HOME}/env/%s_EnvTop.svh       \n"%(tb_name))
        tb_filename.write("\n")
        tb_filename.write("${VERIFY_HOME}/testcase/%s_TestTop.svh \n"%(tb_name))
        tb_filename.write("                                       \n")
        tb_filename.write("${VERIFY_HOME}/tb/tb_top.sv            \n")
        # if self.crg_gen_sv_enable:
        #     tb_filename.write("${VERIFY_HOME}/tb/crg_gen.sv       \n")
        # if self.uvmconfigdb_sv_enable:
        #     tb_filename.write("${VERIFY_HOME}/tb/uvmconfigdb.sv   \n")
        # if self.dutinst_sv_enable:
        #     tb_filename.write("${VERIFY_HOME}/tb/dutinst.sv       \n")
        # if self.dumpctrl_sv_enable:
        #     tb_filename.write("${VERIFY_HOME}/tb/dumpctrl.sv      \n")
        tb_filename.close()
        # vip.f
        #vip_filename = open("vip.f", "w+")
        vip_filename = open(Parameters.Filelist_vip, "w+")

        vip_filename.write("+define+UVM_PACKER_MAX_BYTES=1500000\n")
        vip_filename.write("+define+SVT_UVM_TECHNOLOGY\n")
        vip_filename.write("+define+SVT_FSDB_ENABLE\n")
        vip_filename.write("+define+UVM_DISABLE_AUTO_ITEM_RECORDING\n")
        vip_filename.write("+define+SYNOPSYS_SV\n")
        vip_filename.write("//Disable AXI coveragroup\n")
        vip_filename.write("+define+SVT_AXI_MON_CFG_BASED_COV_GRP_dEF\n")
        if self.VIP_DB['AXI']['Enable']:
            vip_filename.write("//======================AXI=========================================\n")
            vip_filename.write("//*   By default,16 master and 16 slave interfaces are defined      *\n")
            vip_filename.write("//*   in the top level interface.Currently, the maximum master      *\n")
            vip_filename.write("//*   and slave interfaces supported is 450. The number of master   *\n")
            vip_filename.write("//*   and slave interfaces in top level interface can be controlled *\n")
            vip_filename.write("//*   using macros SVT_AXI_MAX_NUM_MASTERS_{0..450} and             *\n")
            vip_filename.write("//*   SVT_AXI_MAX_NUM_SLAVES_{0..450} respectively. For example, if *\n")
            vip_filename.write("//*   you want to use 8 master interfaces and 10 slave interfaces,  *\n")
            vip_filename.write("//*   you can define following macros when compiling the VIP:       *\n")
            vip_filename.write("//*       <li> SVT_AXI_MAX_NUM_MASTERS_8<br>                        *\n")
            vip_filename.write("//*       <li> SVT_AXI_MAX_NUM_SLAVES_10<br>                        *\n")
            vip_filename.write("//==================================================================\n")
            vip_filename.write("//add the AXI vip setting&latency here!!!\n")
            vip_filename.write("//+define+SVT_AXI_MAX_NUM_MASTERS_%s\n"%self.VIP_DB['AXI']['VipMasterNum'])
            vip_filename.write("//+define+SVT_AXI_MAX_NUM_SLAVES_%s\n"%self.VIP_DB['AXI']['VipSlaveNum'])
            vip_filename.write("//+define+SVT_AXI_MAX_DATA_WIDTH=2048\n")
            vip_filename.write("//+define+SVT_AXI_MAX_DATA_USER_WIDTH=2048\n")
            vip_filename.write("//+define+SVT_AXI_MAX_ADDR_WIDTH=64\n")
            vip_filename.write("//+define+SVT_AXI_MAX_ADDR_USER_WIDTH=64\n")
            vip_filename.write("//+define+SVT_AXI_MAX_ID_WIDTH=16\n")
            vip_filename.write("//+define+SVT_AXI_MAX_SIZE_WIDTH=8\n")
            vip_filename.write("//+define+SVT_AXI_MAX_RESP_WIDTH=2\n")
            vip_filename.write("//+define+SVT_AXI_MAX_BURST_LENGTH_WIDTH=8\n")
            vip_filename.write("//+define+SVT_AXI_MAX_NUM_OUTSTANDING_XACT=8192\n")
            vip_filename.write("//+define+SVT_AXI_MAX_NUM_OUTSTANDING_SNOOP_XACT=8192\n")
            vip_filename.write("//+define+SVT_AXI_LOCK_WIDTH=1\n")
            vip_filename.write("//+define+SVT_AXI_MAX_ADDR_DELAY=2000\n")
            vip_filename.write("//+define+SVT_AXI_MAX_ADDR_VALID_DELAY=2000\n")
            vip_filename.write("//+define+SVT_AXI_MAX_WVALID_DELAY=2000\n")
            vip_filename.write("//+define+SVT_AXI_MAX_RVALID_DELAY=2000\n")
            vip_filename.write("//+define+SVT_AXI_MAX_RREADY_DELAY=2000\n")
            vip_filename.write("//+define+SVT_AXI_MAX_WREADY_DELAY=2000\n")
            vip_filename.write("//+define+SVT_AXI_MIN_WRITE_RESP_DELAY=0\n")
            vip_filename.write("//+define+SVT_AXI_MAX_WRITE_RESP_DELAY=2000\n")
            vip_filename.write("//+define+SVT_AXI_MIN_READ_RESP_DELAY=0\n")
            vip_filename.write("//+define+SVT_AXI_MAX_READ_RESP_DELAY=2000\n")
            vip_filename.write("\n")
        
        if self.VIP_DB['AHB']['Enable']:
            vip_filename.write("//======================AHB=========================================\n")
            vip_filename.write("//*   By default,16 master and 16 slave interfaces are defined      *\n")
            vip_filename.write("//*   in the top level interface.Currently, the maximum master      *\n")
            vip_filename.write("//*   and slave interfaces supported is 450. The number of master   *\n")
            vip_filename.write("//*   and slave interfaces in top level interface can be controlled *\n")
            vip_filename.write("//*   using macros SVT_AHB_MAX_NUM_MASTERS_{0..128} and             *\n")
            vip_filename.write("//*   SVT_AHB_MAX_NUM_SLAVES_{0..128} respectively. For example, if *\n")
            vip_filename.write("//*   you want to use 8 master interfaces and 10 slave interfaces,  *\n")
            vip_filename.write("//*   you can define following macros when compiling the VIP:       *\n")
            vip_filename.write("//*       <li> SVT_AHB_MAX_NUM_MASTERS_8<br>                        *\n")
            vip_filename.write("//*       <li> SVT_AHB_MAX_NUM_SLAVES_10<br>                        *\n")
            vip_filename.write("//==================================================================\n")
            vip_filename.write("//add the AHB vip setting&latency here!!!\n")
            vip_filename.write("//+define+SVT_AHB_MAX_NUM_MASTERS_%s\n"%self.VIP_DB['AHB']['VipMasterNum'])
            vip_filename.write("//+define+SVT_AHB_MAX_NUM_SLAVES_%s\n"%self.VIP_DB['AHB']['VipSlaveNum'])
            vip_filename.write("//+define+SVT_AHB_MAX_DATA_WIDTH=2048\n")
            vip_filename.write("//+define+SVT_AHB_MAX_DATA_USER_WIDTH=2048\n")
            vip_filename.write("//+define+SVT_AHB_MAX_ADDR_WIDTH=64\n")
            vip_filename.write("//+define+SVT_AHB_MAX_ADDR_USER_WIDTH=64\n")
            vip_filename.write("//+define+SVT_AHB_HMASTER_PORT_WIDTH=8\n")
            vip_filename.write("//+define+SVT_AHB_DEBUG_PORT_WIDTH=8\n")

        if self.VIP_DB['APB']['Enable']:
            vip_filename.write("//======================APB=================================================\n")
            vip_filename.write("//*  APB Interface provides implicit connection between single master        *\n")
            vip_filename.write("//*  and multiple slaves by default. Below macro                             *\n")
            vip_filename.write("//*  SVT_APB_DISCONNECT_TOP_LEVEL_APB_IF_SIGNALS can be defined in order     *\n")
            vip_filename.write("//*  to disable this implicit connection. Following connectivity between     *\n")
            vip_filename.write("//*  master and slave is further divided into 3 different topology.          *\n")
            vip_filename.write("//*  1) CONNECT_TOP_LEVEL_APB_IF_SIGNALS_BASED_ON_PSEL - master              *\n")
            vip_filename.write("//*      signals are driven only to the slave which is selected              *\n")
            vip_filename.write("//*      by psel. Other slaves will be driven 0 for all signals.             *\n")
            vip_filename.write("//*  2) CONNECT_TOP_LEVEL_APB_IF_SIGNALS_BASED_ON_PSEL_FROM_PASSIVE_SLAVE -  *\n")
            vip_filename.write("//*      this connection is only applicable for passive mode. Here passive   *\n")
            vip_filename.write("//*      slave signals are connected to passive master ports.                *\n")
            vip_filename.write("//*  3) if none of the above two macros are defined then each slave          *\n")
            vip_filename.write("//*     receives signals driven by the master directly.                     *\n")
            vip_filename.write("//======================APB=================================================\n")
            vip_filename.write("//+define+SVT_APB_MAX_NUM_SLAVES=16\n")
            vip_filename.write("//+define+SVT_APB_MAX_DATA_WIDTH=32\n")
            vip_filename.write("//+define+SVT_APB_MAX_ADDR_WIDTH=32\n")
            
        # if self.VIP_DB['AXI']['Enable']:
        #     x=[]
        #     y=[]
        #     for MasterSlave in self.VIP_DB_Feature['AXI']:
        #         #print(self.VIP_DB_Feature['AXI'][MasterSlave]['DataWidth'])
        #         x.append(self.VIP_DB_Feature['AXI'][MasterSlave]['DataWidth'])
        #         y.append(self.VIP_DB_Feature['AXI'][MasterSlave]['AddrWidth'])
        #     max_index, max_DataWidth = max(enumerate(x), key=operator.itemgetter(1))
        #     max_index, max_AddrWidth = max(enumerate(y), key=operator.itemgetter(1))

        #     vip_filename.write("+define+SVT_AXI_MAX_DATA_WIDTH=%s\n"%max_DataWidth)
        #     vip_filename.write("+define+SVT_AXI_MAX_ADDR_WIDTH=%s\n"%max_AddrWidth)

        vip_filename.write("\n")
        vip_filename.write("//+incdir+${XX_VIP_HOME}/include     \n")
        vip_filename.write("//+incdir+${XX_VIP_HOME}/vcs         \n")

        # Title="VipPath"
        # #if self.vip_apb_enable:
        # VipName="APB"
        # if self.VIP_DB[VipName]['Enable']:
        #     vip_filename.write("//APB VIP \n")
        #     vip_filename.write("+incdir+%s/lib/include/sverilog \n"         %self.VIP_DB[VipName][Title])#%self.VIP_apb_path)
        #     vip_filename.write("+incdir+%s/lib/src/sverilog/vcs \n"         %self.VIP_DB[VipName][Title])#%self.VIP_apb_path)
        #     vip_filename.write("%s/lib/include/sverilog/svt_apb.uvm.pkg \n" %self.VIP_DB[VipName][Title])#%self.VIP_apb_path)
        #     vip_filename.write("%s/lib/include/sverilog/svt_apb_if.svi \n"  %self.VIP_DB[VipName][Title])#%self.VIP_apb_path)
        
        # #if self.vip_ahb_enable:
        # VipName="AHB"
        # if self.VIP_DB[VipName]['Enable']:
        #     vip_filename.write("//AHB VIP \n")
        #     vip_filename.write("+incdir+%s/lib/include/sverilog \n"         %self.VIP_DB[VipName][Title])#%self.VIP_ahb_path)
        #     vip_filename.write("+incdir+%s/lib/src/sverilog/vcs \n"         %self.VIP_DB[VipName][Title])#%self.VIP_ahb_path)
        #     vip_filename.write("%s/lib/include/sverilog/svt_ahb.uvm.pkg \n" %self.VIP_DB[VipName][Title])#%self.VIP_ahb_path)
        #     vip_filename.write("%s/lib/include/sverilog/svt_ahb_if.svi \n"  %self.VIP_DB[VipName][Title])#%self.VIP_ahb_path)
        
        # #if self.vip_axi_enable:
        # VipName="AXI"
        # if self.VIP_DB[VipName]['Enable']:
        #     vip_filename.write("//AXI VIP \n")
        #     vip_filename.write("+incdir+%s/lib/include/sverilog \n"         %self.VIP_DB[VipName][Title])#%self.VIP_axi_path)
        #     vip_filename.write("+incdir+%s/lib/src/sverilog/vcs \n"         %self.VIP_DB[VipName][Title])#%self.VIP_axi_path)
        #     vip_filename.write("%s/lib/include/sverilog/svt_axi.uvm.pkg \n" %self.VIP_DB[VipName][Title])#%self.VIP_axi_path)
        #     vip_filename.write("%s/lib/include/sverilog/svt_axi_if.svi \n"  %self.VIP_DB[VipName][Title])#%self.VIP_axi_path)
        # #if self.vip_uart_enable:
        # VipName="UART"
        # if self.VIP_DB[VipName]['Enable']:
        #     vip_filename.write("//UART VIP \n")
        #     vip_filename.write("+incdir+%s/lib/include/sverilog \n"         %self.VIP_DB[VipName][Title])#%self.VIP_uart_path)
        #     vip_filename.write("+incdir+%s/lib/src/sverilog/vcs \n"         %self.VIP_DB[VipName][Title])#%self.VIP_uart_path)
        #     vip_filename.write("%s/lib/include/sverilog/svt_uart.uvm.pkg \n"%self.VIP_DB[VipName][Title])#%self.VIP_uart_path)
        #     vip_filename.write("%s/lib/include/sverilog/svt_uart_if.svi \n" %self.VIP_DB[VipName][Title])#%self.VIP_uart_path)
        
        # #if self.vip_i2c_enable:
        # VipName="I2C"
        # if self.VIP_DB[VipName]['Enable']:
        #     vip_filename.write("//I2C VIP \n")
        #     vip_filename.write("+incdir+%s/lib/include/sverilog \n"         %self.VIP_DB[VipName][Title])#%self.VIP_i2c_path)
        #     vip_filename.write("+incdir+%s/lib/src/sverilog/vcs \n"         %self.VIP_DB[VipName][Title])#%self.VIP_i2c_path)
        #     vip_filename.write("%s/lib/include/sverilog/svt_i2c.uvm.pkg \n" %self.VIP_DB[VipName][Title])#%self.VIP_i2c_path)
        #     vip_filename.write("%s/lib/include/sverilog/svt_i2c_if.svi \n"  %self.VIP_DB[VipName][Title])#%self.VIP_i2c_path)
        
        # #if self.vip_i2s_enable:
        # VipName="I2S"
        # if self.VIP_DB[VipName]['Enable']:
        #     vip_filename.write("//I2S VIP \n")
        #     vip_filename.write("+incdir+%s/lib/include/sverilog \n"         %self.VIP_DB[VipName][Title])#%self.VIP_i2s_path)
        #     vip_filename.write("+incdir+%s/lib/src/sverilog/vcs \n"         %self.VIP_DB[VipName][Title])#%self.VIP_i2s_path)
        #     vip_filename.write("%s/lib/include/sverilog/svt_i2s.uvm.pkg \n" %self.VIP_DB[VipName][Title])#%self.VIP_i2s_path)
        #     vip_filename.write("%s/lib/include/sverilog/svt_i2s_if.svi \n"  %self.VIP_DB[VipName][Title])#%self.VIP_i2s_path)

        for VipName in self.VIP_DB.keys():
            if self.VIP_DB[VipName]['Enable']:
                Title="VipPath"
                vip_filename.write("\n")
                vip_filename.write("//%s VIP \n"%VipName)
                vip_filename.write("+incdir+%s/lib/include/sverilog \n"         %self.VIP_DB[VipName][Title])
                vip_filename.write("+incdir+%s/lib/src/sverilog/vcs \n"         %self.VIP_DB[VipName][Title])
                vip_filename.write("%s/lib/include/sverilog/svt_%s.uvm.pkg \n"  %(self.VIP_DB[VipName][Title],VipName.lower()))
                vip_filename.write("%s/lib/include/sverilog/svt_%s_if.svi \n"   %(self.VIP_DB[VipName][Title],VipName.lower()))
            
                #if self.VIP_DB['AXI']['Enable']:
                if VipName=='AXI':
                    x=[]
                    y=[]
                    for MasterSlave in self.VIP_DB_Feature['AXI']:
                        #print(self.VIP_DB_Feature['AXI'][MasterSlave]['DataWidth'])
                        x.append(self.VIP_DB_Feature['AXI'][MasterSlave]['DataWidth'])
                        y.append(self.VIP_DB_Feature['AXI'][MasterSlave]['AddrWidth'])
                    max_index, max_DataWidth = max(enumerate(x), key=operator.itemgetter(1))
                    max_index, max_AddrWidth = max(enumerate(y), key=operator.itemgetter(1))

                    vip_filename.write("+define+SVT_AXI_MAX_DATA_WIDTH=%s\n"%max_DataWidth)
                    vip_filename.write("+define+SVT_AXI_MAX_ADDR_WIDTH=%s\n"%max_AddrWidth)
        
        vip_filename.write("\n")
        vip_filename.close()
        
        # cmodel.f
        #cmodel_filename = open("cmodel.f", "w+")
        cmodel_filename = open(Parameters.Filelist_cmodel, "w+")
        cmodel_filename.write("////add the cmodel lib file and cmodel file here!!!        \n")
        cmodel_filename.write("//+incdir+${VERIFY_HOME}/reference/xx_dir \n")
        cmodel_filename.write("//${VERIFY_HOME}/reference/xx.c           \n")
        cmodel_filename.write("//${VERIFY_HOME}/reference/xx.cpp         \n")
        cmodel_filename.write("//${VERIFY_HOME}/reference/xx.a           \n")
        cmodel_filename.write("//${VERIFY_HOME}/reference/xx.so          \n")
        cmodel_filename.write("////add C compile options                 \n")
        cmodel_filename.write("//C99                                     \n")
        cmodel_filename.close()

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
    gen=gen_filelist_file()