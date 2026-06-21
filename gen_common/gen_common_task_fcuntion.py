#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os

class gen_common_task_function:

    def __init__(self):
        print("[gen_common_task_function]:initial")
        self.gen_common_task_function_info(name=None,PrintEnable=True)

    def gen_common_task_function_info(self,name,PrintEnable):
        if name==None:
            filename = open("common_task_function.sv", "w+")
        else:
            filename = open("%s_common_task_function.sv"%name, "w+")
        filename.write("\n")
        ###################################################################################
        filename.write("function void ReadFile(input string filename,output bit[63:0]UserDataQueue[$]);\n")
        filename.write("\tinteger fr;\n")
        filename.write("\tinteger res;\n")
        filename.write("\tlogic[63:0]data;\n")
        filename.write("\tstring str;\n")
        filename.write("\n")
        filename.write("\tfr=$fopen(filename,\"r\");\n")
        filename.write("\tif(fr==0)begin\n")
        filename.write("\t\t$display(\"%s cannt read file!\",filename);\n")
        filename.write("\t\t$finish();\n")
        filename.write("\tend\n")
        filename.write("\n")
        filename.write("\twhile(!$feof(fr))begin\n")
        filename.write("\t\tres=$fscanf(fr,\"%h\",data);\n")
        filename.write("\t\t//$display(\"debug:data=%h\\n\",data);\n")
        filename.write("\t\tUserDataQueue.push_back(data);\n")
        filename.write("\tend\n")
        filename.write("\t//$display(\"debug:data size=%h\\n\",UserDataQueue.size());\n")
        filename.write("\n")
        filename.write("\t$fclose(fr);\n")
        filename.write("\n")
        filename.write("endfunction\n")
        filename.write("\n")
        ###################################################################################
        filename.write("function void ReadCfgFile(input string CfgFileName);\n")
        filename.write("\tinteger      fr;\n")
        filename.write("\tbit[1023:0]   data;\n")
        filename.write("\tstring        str;\n")
        filename.write("\n")
        filename.write("\tbit[1023:0]CfgData[string];\n")
        filename.write("\n")
        filename.write("\tfr=$fopen(CfgFileName,\"r\");\n")
        filename.write("\tif(fr==0)begin\n")
        filename.write("\t\t$display(\"%s cann't read!!!\",CfgFileName);\n")
        filename.write("\t\t$finish();\n")
        filename.write("\tend\n")
        filename.write("\n")
        filename.write("\twhile(!$feof(fr))begin\n")
        filename.write("\t\t$fscanf(fr,\"%s %h\",str,data);\n")
        filename.write("\t\t//%s_cfg.CfgData[str]=data;\n"%name)
        filename.write("\t\tCfgData[str]=data;\n")
        filename.write("\tend\n")
        filename.write("\t$fclose(fr);\n")
        filename.write("endfunction\n")
        filename.write("\n")
        filename.close()
        ###################################################################################
        filename.close()

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")


if __name__ == '__main__':
    gen=gen_common_task_function()