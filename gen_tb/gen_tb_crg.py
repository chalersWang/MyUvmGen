#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from readexcel.readexcel_ClockRst import readexcel_ClockRst
from common_lib.parameters import Parameters

class gen_tb_crg:

    def __init__(self):
        print("[gen_tb_crg]:initial")
        #EnvironmentGenCfg='../VerifyEnvironmentGenCfg.xlsx'
        EnvironmentGenCfg=Parameters.EnvironmentGenCfg
        readexcel_ClockRst.readexcel_ClockRst_info(self,EnvironmentGenCfg,PrintEnable=False)
        self.gen_tb_crg_info(None,self.Clk_name,self.Clk_period,self.Rst_name,self.Rst_release,PrintEnable=True)

    def gen_tb_crg_info(self,FileName,Clk_name,Clk_period,Rst_name,Rst_release,PrintEnable):
        if FileName==None:
            filename = open('crg_gen.sv', "w+",encoding='utf-8')
        else:
            filename=FileName

        ################## clk ######################################
        filename.write("\n")
        filename.write("// -------------------------------------\n")
        filename.write("//| crg_gen:clk                         |\n")
        filename.write("// -------------------------------------\n")
        for i in range(0,len(Clk_name)):
            filename.write("reg  %s;\n" %Clk_name[i])
        filename.write("                                 \n")
        filename.write("initial begin                    \n")
        filename.write("     #10ns;                      \n")
        for i in range(0,len(Clk_name)):
            filename.write("     %s=1'b1;                \n" %Clk_name[i])
        filename.write("end                              \n")
        for i in range(0,len(Clk_name)):
            filename.write("always #(%sns/2.0) %s=~%s;   \n" %(Clk_period[i],Clk_name[i],Clk_name[i]))
        filename.write("\n")
        
        ################## rst ######################################
        filename.write("// -------------------------------------\n")
        filename.write("//| crg_gen:rst                         |\n")
        filename.write("//| Note :axi vip rst > 32 cycle        |\n")
        filename.write("// -------------------------------------\n")
        for i in range(0,len(Rst_name)):
            filename.write("reg  %s;                     \n" %Rst_name[i])
        filename.write("                                 \n")
        filename.write("initial begin                    \n")
        for i in range(0,len(Rst_name)):
            filename.write("     %s=1'b0;                \n" %Rst_name[i])
        filename.write("     fork                        \n")
        for i in range(0,len(Rst_name)):
            filename.write("         begin               \n")
            filename.write("             #%sns;          \n" %Rst_release[i])
            filename.write("             %s=1'b1;        \n" %Rst_name[i])
            filename.write("             $display(\"%s ns [%s] Release!!!\",$time);\n"%("%0d",Rst_name[i]))
            filename.write("         end                 \n")
        filename.write("     join                        \n")
        filename.write("end                              \n")
        filename.write("\n")

        ################## fininal_block######################################
        filename.write("// --------------------------------------------------\n")
        filename.write("//| final block\n")
        filename.write("//| (1)一种特殊的构造块\n")
        filename.write("//| (2)仿真结束时执行,即在所有initial块执行完后执行\n")
        filename.write("//| (3)零仿真时间内执行,故内部不能有任何延迟或等待语句\n")
        filename.write("//| (4)仿真工具调用$finish时,自动被执行\n")
        filename.write("//| (5)可在finial块种执行特定代码,如提示信息/警告/报告等\n")
        filename.write("//| 除此之外还有 final class\n")
        filename.write("//| (1)详见 https://mp.weixin.qq.com/s/1XR7Bn2igY-hxj8rC9Xqlg\n")
        filename.write("// --------------------------------------------------\n")
        filename.write("final begin\n")
        filename.write("    $display(\"Please adding info/operation what you want to add!!!\");\n")
        filename.write("end\n")

        if FileName==None:
            filename.close()

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")

if __name__ == '__main__':
    gen=gen_tb_crg()