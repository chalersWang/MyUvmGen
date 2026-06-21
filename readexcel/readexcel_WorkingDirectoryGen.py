#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import openpyxl
import sys
import os
from common_lib.parameters import Parameters
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from common_lib.common_lib import getFileEnable

class readexcel_WorkingDirectoryGen:

    def __init__(self):
        EnvironmentGenCfg='VerifyEnvironmentGenCfg.xlsx'
        print("[readexcel_WorkingDirectoryGen]:initiail")
        self.readexcel_WorkingDirectoryGen_info(EnvironmentGenCfg,PrintEnable=True)

    def readexcel_WorkingDirectoryGen_info(self,EnvironmentGenCfg,PrintEnable):

        wb = openpyxl.load_workbook(EnvironmentGenCfg)
        sheet=wb['WorkingDirectoryGen']
        ProjectName =sheet['A']
        Level1      =sheet['B']
        Level2      =sheet['C']
        Level3      =sheet['D']
        Description =sheet['E']
        Enable      =sheet['F']
        if Parameters.tb_name!='xx' and Parameters.tb_name!=None:
            self.tb_name=Parameters.tb_name
        else:
            if sheet['A3'].value!='xx' and sheet['A3'].value!=None and sheet['A3'].value!='' and sheet['A3'].value!=[]:
                self.tb_name=sheet['A3'].value
            else:
               self.tb_name='prj_wx' 

        # # file of cfg dir
        # self.ut_xx_cfg_enable=self.getFileEnable(Level2,'ut_xx.cfg',Enable)
        # self.it_xx_cfg_enable=self.getFileEnable(Level2,'it_xx.cfg',Enable)
        # self.st_xx_cfg_enable=self.getFileEnable(Level2,'st_xx.cfg',Enable)
        # # file of tb dir
        # self.crg_gen_sv_enable=self.getFileEnable(Level2,'crg_gen.sv',Enable)
        # self.uvmconfigdb_sv_enable=self.getFileEnable(Level2,'uvmconfigdb.sv',Enable)
        # self.dutinst_sv_enable=self.getFileEnable(Level2,'dutinst.sv',Enable)
        # self.dumpctrl_sv_enable=self.getFileEnable(Level2,'dumpctrl.sv',Enable)
        # # file of sva dir
        # #self.interfacemacro_enable=self.getFileEnable(Level2,'interfacemacro.sv',Enable)
        # #self.xx_vif_enable=self.getFileEnable(Level2,'xx_vif.sv',Enable)
        # self.sva_code_enable=self.getFileEnable(Level2,'sva_code',Enable)
        # # file of testplan dir
        # self.sxx_base_group_enable=self.getFileEnable(Level2,'xx_base_group',Enable)
            
        # file of cfg dir
        # self.ut_xx_cfg_enable       =getFileEnable(self,Level2,'ut_xx.cfg',Enable)
        # self.it_xx_cfg_enable       =getFileEnable(self,Level2,'it_xx.cfg',Enable)
        # self.st_xx_cfg_enable       =getFileEnable(self,Level2,'st_xx.cfg',Enable)
        # file of tb dir
        self.crg_gen_sv_enable      =getFileEnable(self,Level2,'crg_gen.sv',Enable)
        self.uvmconfigdb_sv_enable  =getFileEnable(self,Level2,'uvmconfigdb.sv',Enable)
        self.dutinst_sv_enable      =getFileEnable(self,Level2,'dutinst.sv',Enable)
        self.dumpctrl_sv_enable     =getFileEnable(self,Level2,'dumpctrl.sv',Enable)
        # file of sva dir
        #self.interfacemacro_enable =getFileEnable(self,Level2,'interfacemacro.sv',Enable)
        #self.xx_vif_enable         =getFileEnable(self,Level2,'xx_vif.sv',Enable)
        self.sva_code_enable        =getFileEnable(self,Level2,'sva_code',Enable)
        # file of testplan dir
        self.sxx_base_group_enable  =getFileEnable(self,Level2,'xx_base_group',Enable)

        if PrintEnable==True:
            ProjectNameStr  ='ProjectName'
            Level1Str       ='Level1 Directory'
            Level2Str       ='Level2 Directory'
            Level3Str       ='Level3 Directory'
            EnableStr       ='Enable'
            print("--------------------------------------------------------------")
            print("|  %-10s  |  %-10s  |  %-10s  |  %-10s  |"%(ProjectNameStr,Level1Str,Level2Str,EnableStr))
            for i in range(2,len(Enable)):
                if ProjectName[i].value==None:
                    ProjectNameStr=''
                else:
                    ProjectNameStr='%s'%ProjectName[i].value
                
                if Level1[i].value==None:
                    Level1Str=''
                else:
                    Level1Str='%s'%Level1[i].value
                
                if Level2[i].value==None:
                    Level2Str=''
                else:
                    Level2Str='%s'%Level2[i].value

                print("%-20s %-20s %-20s %-20s"%(ProjectNameStr,Level1Str,Level2Str,Enable[i].value))

    # def getFileEnable(self,TitleName,FileName,Enable):
    #     for filename in TitleName:
    #         if filename.value == FileName:
    #             for EN in Enable:
    #                 if EN.row == filename.row:
    #                     enable=EN.value
    #     return enable

if __name__ == '__main__':
    gen=readexcel_WorkingDirectoryGen()