#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import openpyxl
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from common_lib.common_lib import ExtractArray

class readexcel_VIP:

    def __init__(self):
        EnvironmentGenCfg='../VerifyEnvironmentGenCfg.xlsx'
        print("[readexcel_VIP]:initiail")
        self.readexcel_VIP_info(EnvironmentGenCfg,PrintEnable=True)
        self.readexcel_VIP_AXI_info(EnvironmentGenCfg,PrintEnable=True)

    def readexcel_VIP_info(self,EnvironmentGenCfg,PrintEnable):

        wb = openpyxl.load_workbook(EnvironmentGenCfg)
        sheet           =wb['VIP']
        VIP_type        =sheet['A']
        VIP_name        =sheet['B']
        self.VIP_name   =sheet['B']
        VIP_enable      =sheet['C']
        VIP_MasterNum   =sheet['D']
        VIP_SlaveNum    =sheet['E']
        VIP_Path        =sheet['F']
        VIP_Features    =sheet['G']

        #=============================================================================================
        # #[VIP_TYPE]:NetworkOnChip
        # self.vip_apb_enable         =self.getFileEnable(VIP_name,'APB',VIP_enable)
        # self.vip_ahb_enable         =self.getFileEnable(VIP_name,'AHB',VIP_enable)
        # self.vip_axi_enable         =self.getFileEnable(VIP_name,'AXI',VIP_enable)
        # self.vip_ccix_enable        =self.getFileEnable(VIP_name,'CCIX',VIP_enable)
        # self.vip_cxl_enable         =self.getFileEnable(VIP_name,'CXL',VIP_enable)
        # #[VIP_TYPE]:LowSpeedInterface
        # self.vip_uart_enable        =self.getFileEnable(VIP_name,'UART',VIP_enable)
        # self.vip_spi_enable         =self.getFileEnable(VIP_name,'SPI',VIP_enable)
        # self.vip_i2c_enable         =self.getFileEnable(VIP_name,'I2C',VIP_enable)
        # self.vip_i2s_enable         =self.getFileEnable(VIP_name,'I2S',VIP_enable)
        # self.vip_can_enable         =self.getFileEnable(VIP_name,'CAN',VIP_enable)
        # #[VIP_TYPE]:HighSpeedInterface
        # self.vip_usb_enable         =self.getFileEnable(VIP_name,'USB',VIP_enable)
        # self.vip_pcie_enable        =self.getFileEnable(VIP_name,'PCIE',VIP_enable)
        # self.vip_ethernet_enable    =self.getFileEnable(VIP_name,'Ethernet',VIP_enable)
        # #[VIP_TYPE]:MemoryInterface
        # self.vip_emmc_enable        =self.getFileEnable(VIP_name,'EMMC',VIP_enable)
        # self.vip_ddr_enable         =self.getFileEnable(VIP_name,'DDR',VIP_enable)
        # self.vip_lpddr_enable       =self.getFileEnable(VIP_name,'LPDDR',VIP_enable)
        # self.vip_gddr_enable        =self.getFileEnable(VIP_name,'GDDR',VIP_enable)
        # self.vip_hbm_enable         =self.getFileEnable(VIP_name,'HBM',VIP_enable)
        # #[VIP_TYPE]:ElseInterface
        # self.vip_jtag_enable        =self.getFileEnable(VIP_name,'Jtag',VIP_enable)
        # self.vip_coresight_enable   =self.getFileEnable(VIP_name,'Coresight',VIP_enable)
        # self.vip_hdmi_enable        =self.getFileEnable(VIP_name,'HDMI',VIP_enable)
        # self.vip_dp_enable          =self.getFileEnable(VIP_name,'DP',VIP_enable)

        # #apb vip
        # self.VIP_apb_master_num     =self.getVipNum(VIP_name,'APB',VIP_MasterNum)
        # self.VIP_apb_slave_num      =self.getVipNum(VIP_name,'APB',VIP_SlaveNum)
        # #ahb vip
        # self.VIP_ahb_master_num     =self.getVipNum(VIP_name,'AHB',VIP_MasterNum)
        # self.VIP_ahb_slave_num      =self.getVipNum(VIP_name,'AHB',VIP_SlaveNum)
        # #axi vip
        # self.VIP_axi_master_num     =self.getVipNum(VIP_name,'AXI',VIP_MasterNum)
        # self.VIP_axi_slave_num      =self.getVipNum(VIP_name,'AXI',VIP_SlaveNum)

        # for i in range(len(VIP_name)):
        #     #[VIP_TYPE]:NetworkOnChip
        #     if VIP_name[i].value=='APB'         :   self.VIP_apb_path       =VIP_Path[i].value
        #     if VIP_name[i].value=='AHB'         :   self.VIP_ahb_path       =VIP_Path[i].value
        #     if VIP_name[i].value=='AXI'         :   self.VIP_axi_path       =VIP_Path[i].value
        #     if VIP_name[i].value=='CCIX'        :   self.VIP_ccix_path      =VIP_Path[i].value
        #     if VIP_name[i].value=='CXL'         :   self.VIP_cxl_path       =VIP_Path[i].value
        #     #[VIP_TYPE]:LowSpeedInterface
        #     if VIP_name[i].value=='UART'        :   self.VIP_uart_path      =VIP_Path[i].value
        #     if VIP_name[i].value=='SPI'         :   self.VIP_spi_path       =VIP_Path[i].value
        #     if VIP_name[i].value=='I2C'         :   self.VIP_i2c_path       =VIP_Path[i].value
        #     if VIP_name[i].value=='I2S'         :   self.VIP_i2s_path       =VIP_Path[i].value
        #     if VIP_name[i].value=='CAN'         :   self.VIP_can_path       =VIP_Path[i].value
        #     #[VIP_TYPE]:HighSpeedInterface
        #     if VIP_name[i].value=='USB'         :   self.VIP_usb_path       =VIP_Path[i].value
        #     if VIP_name[i].value=='PCIE'        :   self.VIP_pcie_path      =VIP_Path[i].value
        #     if VIP_name[i].value=='Ethernet'    :   self.VIP_ethernet_path  =VIP_Path[i].value
        #     #[VIP_TYPE]:MemoryInterface
        #     if VIP_name[i].value=='EMMC'        :   self.VIP_emmc_path      =VIP_Path[i].value
        #     if VIP_name[i].value=='DDR'         :   self.VIP_ddr_path       =VIP_Path[i].value
        #     if VIP_name[i].value=='LPDDR'       :   self.VIP_lpddr_path     =VIP_Path[i].value
        #     if VIP_name[i].value=='GDDR'        :   self.VIP_gddr_path      =VIP_Path[i].value
        #     if VIP_name[i].value=='HBM'         :   self.VIP_hbm_path       =VIP_Path[i].value
        #     #[VIP_TYPE]:ElseInterface
        #     if VIP_name[i].value=='Jtag'        :   self.VIP_jtag_path      =VIP_Path[i].value
        #     if VIP_name[i].value=='Coresight'   :   self.VIP_coresight_path =VIP_Path[i].value
        #     if VIP_name[i].value=='HDMI'        :   self.VIP_hdmi_path      =VIP_Path[i].value
        #     if VIP_name[i].value=='DP'          :   self.VIP_dp_path        =VIP_Path[i].value

        #=============================================================================================
        # vipname         =self.ExtractArray(VIP_name         ,"VIP_name")
        # Enable          =self.ExtractArray(VIP_enable       ,"Enable")
        # VipMasterNum    =self.ExtractArray(VIP_MasterNum    ,"VipMasterNum")
        # VipSlaveNum     =self.ExtractArray(VIP_SlaveNum     ,"VipSlaveNum")
        # VipPath         =self.ExtractArray(VIP_Path         ,"VipPath")

        vipname         =ExtractArray(self,VIP_name         ,"VIP_name")
        Enable          =ExtractArray(self,VIP_enable       ,"Enable")
        VipMasterNum    =ExtractArray(self,VIP_MasterNum    ,"VipMasterNum")
        VipSlaveNum     =ExtractArray(self,VIP_SlaveNum     ,"VipSlaveNum")
        VipPath         =ExtractArray(self,VIP_Path         ,"VipPath")

        vipdb={}
        for i in range(len(vipname)):
            vipdb[vipname[i]]={}
            vipdb[vipname[i]]['Enable']         =Enable[i]
            vipdb[vipname[i]]['VipMasterNum']   =VipMasterNum[i]
            vipdb[vipname[i]]['VipSlaveNum']    =VipSlaveNum[i]
            vipdb[vipname[i]]['VipPath']        =VipPath[i]

        self.VIP_DB=vipdb

        if PrintEnable==True:
            print("===================================================================")
            print("%-15s%-15s%-15s%-15s%-15s"%("VIP_name","Enable","VipMasterNum","VipSlaveNum","VipPath"))
            # for i in range(1,len(VIP_name)):
            #     print("%-15s%-15s%-15s%-15s%-15s"
            #           %(VIP_name[i].value,VIP_enable[i].value,VIP_MasterNum[i].value,VIP_SlaveNum[i].value,VIP_Path[i].value))
            for i in range(len(vipname)):
                print("%-15s%-15s%-15s%-15s%-15s"
                      %(vipname[i],Enable[i],VipMasterNum[i],VipSlaveNum[i],VipPath[i]))
        

    def readexcel_VIP_AXI_info(self,EnvironmentGenCfg,PrintEnable):

        wb = openpyxl.load_workbook(EnvironmentGenCfg)
        sheet           =wb['VIP_Features']
        VIP_name        =sheet['A']
        MasterSlave     =sheet['B']
        AddrWidth       =sheet['C']
        DataWidth       =sheet['D']
        IdWidth         =sheet['E']
        Outstanding     =sheet['F']
        BurstType       =sheet['G']
        NarrowType      =sheet['H']

        # vipname         =self.ExtractArray(VIP_name     ,"VIP_name")
        # masterslave     =self.ExtractArray(MasterSlave  ,"MasterSlave")
        # addrwidth       =self.ExtractArray(AddrWidth    ,"AddrWidth")
        # datawidth       =self.ExtractArray(DataWidth    ,"DataWidth")
        # idwidth         =self.ExtractArray(IdWidth      ,"IdWidth")
        # outstanding     =self.ExtractArray(Outstanding  ,"Outstanding")
        # bursttype       =self.ExtractArray(BurstType    ,"BurstType")
        # narrowtype      =self.ExtractArray(NarrowType   ,"NarrowType")

        vipname         =ExtractArray(self,VIP_name     ,"VIP_name")
        masterslave     =ExtractArray(self,MasterSlave  ,"MasterSlave")
        addrwidth       =ExtractArray(self,AddrWidth    ,"AddrWidth")
        datawidth       =ExtractArray(self,DataWidth    ,"DataWidth")
        idwidth         =ExtractArray(self,IdWidth      ,"IdWidth")
        outstanding     =ExtractArray(self,Outstanding  ,"Outstanding")
        bursttype       =ExtractArray(self,BurstType    ,"BurstType")
        narrowtype      =ExtractArray(self,NarrowType   ,"NarrowType")

        vipdb={}
        vipdb['APB']={}
        vipdb['AHB']={}
        vipdb['AXI']={}
        for i in range(0,len(vipname)-1):
            vipdb[vipname[i]][masterslave[i]]={}
            vipdb[vipname[i]][masterslave[i]]['AddrWidth']   =addrwidth[i]
            vipdb[vipname[i]][masterslave[i]]['DataWidth']   =datawidth[i]
            vipdb[vipname[i]][masterslave[i]]['IdWidth']     =idwidth[i]
            vipdb[vipname[i]][masterslave[i]]['Outstanding'] =outstanding[i]
            vipdb[vipname[i]][masterslave[i]]['BurstType']   =bursttype[i]
            vipdb[vipname[i]][masterslave[i]]['NarrowType']  =narrowtype[i]

        self.VIP_DB_Feature=vipdb
        #print(vipdb['AXI']['Master0']['BurstType'].rsplit(','))

        if PrintEnable==True:
            print("=======================================================================================================================")
            print("%-15s%-15s%-15s%-15s%-15s%-15s%-20s%-20s"%("VIP_name","MasterSlave","AddrWidth","DataWidth","IdWidth","Outstanding","BurstType","NarrowType"))
            for i in range(0,len(vipname)-1):
                print("%-15s%-15s%-15s%-15s%-15s%-15s%-20s%-20s"%(
                    vipname[i],masterslave[i],addrwidth[i],datawidth[i],idwidth[i],outstanding[i],bursttype[i],narrowtype[i]))

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

    # def ExtractArray(self,sheetname,ExtractKeyword):
    #     ExtractKeywordName=[]
    #     for name in sheetname:
    #         if (not name.value ==None)&(not name.value==ExtractKeyword):
    #             ExtractKeywordName.append(name.value)
    #     return ExtractKeywordName

if __name__ == '__main__':
    gen=readexcel_VIP()