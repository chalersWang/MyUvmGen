#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from readexcel.readexcel_DutSignal import readexcel_DutSignal
from common_lib.parameters import Parameters

class gen_tb_dutinst:

    def __init__(self):
        print("[gen_tb_dutinst]:initial")
        #EnvironmentGenCfg='../VerifyEnvironmentGenCfg.xlsx'
        EnvironmentGenCfg=Parameters.EnvironmentGenCfg
        readexcel_DutSignal.readexcel_DutSignal_info(self,EnvironmentGenCfg,PrintEnable=False)
        self.gen_tb_dutinst_info(None,self.DUT_Name,self.DUT_GroupName,self.DUT_Signals,PrintEnable=True)

    def gen_tb_dutinst_info(self,FileName,DUT_Name,Group_Name,DUT_Signals,PrintEnable):
        if FileName==None:
            filename = open('dutinst.sv', "w+")
        else:
            filename=FileName
        
        Signals0=[]
        Signals1=[]
        Signals2=[]
        Signals3=[]
        Signals4=[]
        Signals5=[]
        Signals6=[]
        delaystrlst=[]
        # statement of signals
        filename.write("\n")
        filename.write("//dut inst\n")
        for i in range(0,len(DUT_Signals)):
            Signals0=DUT_Signals[i].replace(',\n',';')
            Signals1=Signals0.replace('input','wire ')
            Signals2=Signals1.replace('output','wire ')
            Signals3=Signals2.replace('inout','wire ')
            for str in Signals3:
                if str==';' or str==',':
                    filename.write(";\n")
                else:
                    filename.write("%s" %str)
            filename.write("\n")
        # inst of DUT
        filename.write("%s DUT(\n" %DUT_Name.value)
        for i in range(0,len(self.DUT_Signals)):
            Signals0=DUT_Signals[i].replace('\n','')
            Signals1=Signals0.replace('input','')
            Signals2=Signals1.replace('output','')
            Signals3=Signals2.replace('inout','')
            Signals4=Signals3.replace(' ','')
            for j in range(100):
                delaystrlst=Signals4[Signals4.find('['):(Signals4.find(']')+1)]
                if delaystrlst==None:
                    break
                else:
                    Signals4=Signals4.replace(delaystrlst,'')
            Signals5=Signals4
            Signals6=Signals5.rstrip(',')
            Signals7=Signals6.split(',')
            for j in range(len(Signals7)):
                if i==(len(self.DUT_Signals)-1) and j==(len(Signals7)-1):
                    # filename.write(".%s\t\t\t(TopVif.%svif.%s\t\t\t)\n" %(Signals7[j],Group_Name[i],Signals7[j]))
                    filename.write(".%s\t\t\t(TopVif.%svif.%s\t\t\t)\n" %(Signals7[j],Group_Name[i],Signals7[j]))
                else:
                    # filename.write(".%s\t\t\t(TopVif.%svif.%s\t\t\t),\n" %(Signals7[j],Group_Name[i],Signals7[j]))
                    filename.write(".%s\t\t\t(TopVif.%svif.%s\t\t\t),\n" %(Signals7[j],Group_Name[i],Signals7[j]))

        filename.write(");\n")
        filename.write("\n")

        if FileName==None:
            filename.close()

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")
    
if __name__ == '__main__':
    gen=gen_tb_dutinst()