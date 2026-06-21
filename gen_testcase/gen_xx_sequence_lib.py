#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os
import sys
import operator
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from readexcel.readexcel_WorkingDirectoryGen import readexcel_WorkingDirectoryGen
from readexcel.readexcel_VIP import readexcel_VIP
# from readexcel.readexcel_DutSignal import readexcel_DutSignal
# from readexcel.readexcel_ClockRst import readexcel_ClockRst

# from common_lib.common_lib import GenVipAxiLibTask
from common_lib.common_lib import GenVipAxiLibTask_Burst
from common_lib.common_lib import GenVipAxiLibTask_NarrowBurst

from common_lib.parameters import Parameters

class gen_xx_sequence_lib:

    def __init__(self):
        print("[gen_xx_sequence_lib]:initial")
        #EnvironmentGenCfg='../VerifyEnvironmentGenCfg.xlsx'
        EnvironmentGenCfg=Parameters.EnvironmentGenCfg
        readexcel_WorkingDirectoryGen.readexcel_WorkingDirectoryGen_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_VIP.readexcel_VIP_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_VIP.readexcel_VIP_AXI_info(self,EnvironmentGenCfg,PrintEnable=False)
        # readexcel_ClockRst.readexcel_ClockRst_info(self,EnvironmentGenCfg,PrintEnable=False)
        # readexcel_DutSignal.readexcel_DutSignal_info(self,EnvironmentGenCfg,PrintEnable=False)
        for VipName in self.VIP_DB.keys():
            if self.VIP_DB[VipName]['Enable']:
                self.gen_xx_common_task_funciton_info(VipName,PrintEnable=True)

    def gen_xx_common_task_funciton_info(self,name,PrintEnable):
        VipName=name.upper()
        
        #apb task
        if VipName=='APB':
            #if self.vip_apb_enable:
            if self.VIP_DB[VipName]['Enable']:
                filename = open("apb_common_task_function.sv", "w+")
                filename.write("\n")
                #for i in range(0,self.VIP_apb_master_num):
                for i in range(self.VIP_DB['APB']['VipMasterNum']):
                    MasterID="Master%s"%i
                    VIP_APB_ADDRWIDTH=self.VIP_DB_Feature['APB'][MasterID]['AddrWidth']
                    VIP_APB_DATAWIDTH=self.VIP_DB_Feature['APB'][MasterID]['DataWidth']
                filename.close()
        
        #ahb task
        if VipName=='AHB':
            #if self.vip_ahb_enable:
            if self.VIP_DB[VipName]['Enable']:
                filename = open("ahb_common_task_function.sv", "w+")
                filename.write("\n")
                #for i in range(0,self.VIP_ahb_master_num):
                for i in range(self.VIP_DB['AHB']['VipMasterNum']):
                    MasterID="Master%s"%i
                    VIP_AHB_ADDRWIDTH=self.VIP_DB_Feature['AHB'][MasterID]['AddrWidth']
                    VIP_AHB_DATAWIDTH=self.VIP_DB_Feature['AHB'][MasterID]['DataWidth']
                filename.close()
        
        #axi task
        if VipName=='AXI':
            #if self.vip_axi_enable:
            if self.VIP_DB[VipName]['Enable']:
                filename = open("axi_common_task_function.sv", "w+")
                filename.write("\n")
                #for i in range(0,self.VIP_axi_master_num):
                for i in range(self.VIP_DB['AXI']['VipMasterNum']):
                    MasterID="Master%s"%i
                    VIP_AXI_ADDRWIDTH=self.VIP_DB_Feature['AXI'][MasterID]['AddrWidth']
                    VIP_AXI_DATAWIDTH=self.VIP_DB_Feature['AXI'][MasterID]['DataWidth']
                    VIP_AXI_BurstType=self.VIP_DB_Feature['AXI'][MasterID]['BurstType'].rsplit(',')
                    VIP_AXI_NarrowType=self.VIP_DB_Feature['AXI'][MasterID]['NarrowType'].rsplit(',')
                    for j in range(len(VIP_AXI_BurstType)):
                        #self.GenVipAxiLibTask(filename,i,int(VIP_AXI_BurstType[j]),VIP_AXI_ADDRWIDTH,VIP_AXI_DATAWIDTH)
                        GenVipAxiLibTask_Burst(self,filename,i,int(VIP_AXI_BurstType[j]),VIP_AXI_ADDRWIDTH,VIP_AXI_DATAWIDTH)
                    GenVipAxiLibTask_NarrowBurst(self,filename,i,VIP_AXI_NarrowType,VIP_AXI_ADDRWIDTH,VIP_AXI_DATAWIDTH)
                filename.close()
        

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")
            
if __name__ == '__main__':
    gen=gen_xx_sequence_lib()