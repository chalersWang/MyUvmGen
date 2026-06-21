#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os
import re
import sys

#sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
# Auto-detect MY_TOOLS_HOME if not set in environment
if "MY_TOOLS_HOME" not in os.environ:
    os.environ["MY_TOOLS_HOME"] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append("%s"%os.environ.get("MY_TOOLS_HOME"))

from read_kfile import read_kfile

class gen_kf_ff:

    def __init__(self):
        print("[gen_kf_ff]:initial")
        self.FileinfoAfterDefine=[]
        filepath='./demo.k'
        read_kfile.read_kfile_info(self,"./demo.cfg",PrintEnable=False)
        self.gen_kf_ff_info(filepath,PrintEnable=True)

    def gen_kf_ff_info(self,filepath,PrintEnable):
        Enable=True
        StoreInfo=[]

        L1_ifdef            =False
        L1_else             =False
        L1_endif            =False
        L1_MatchIf          =False

        L2_ifdef            =False
        L2_else             =False
        L2_endif            =False
        L2_MatchIf          =False

        if os.path.isfile(filepath):

            #with open('%s'%filepath,'r',encoding='utf-8') as f:
            with open('%s'%filepath,'r') as f:
                lines=f.readlines()                
                for i in range(len(lines)):
                    ifdef_lines=re.findall(r"`ifdef(.*?)\n", lines[i].replace(" ",""))
                    esle_lines=re.findall(r"`else(.*?)\n", lines[i].replace(" ",""))
                    endif_lines=re.findall(r"`endif(.*?)\n", lines[i].replace(" ",""))

                    if ifdef_lines!=[]: ifdeflines=ifdef_lines[0];   
                    else:               ifdeflines=None
                    #================================================================================
                    if  L1_ifdef==False and L1_else==False and L1_endif==False :

                        L1_MatchIf=False
                        if re.search(r"`ifdef",lines[i]):
                            #ifdeflines=re.findall(r"`ifdef(.*?)\n", lines[i].replace(" ",""))
                            for j in range(len(self.kfileToffile_define)):
                                self.PrintLog("ifdeflines=%s"%ifdeflines,Enable)
                                self.PrintLog("kfileToffile_define=%s"%self.kfileToffile_define[j],Enable)
                                if ifdeflines==self.kfileToffile_define[j]:
                                    L1_MatchIf=True
                            
                            L1_if_store     =L1_MatchIf
                            L1_else_store   =not L1_if_store#L1_MatchIf
                            StoreInfo.append(False)
                            L1_ifdef=True
                            self.PrintLog("Debug[1]:%s"%lines[i],Enable)
                        else:
                            if re.search(r"`else",lines[i]):
                                print("Error:Keyword `ifdef is missing!!!")
                            else:
                                if re.search(r"`endif",lines[i]):
                                    print("Error:Keyword `ifdef and else is missing!!!")
                                else:
                                    StoreInfo.append(True)
                                    self.PrintLog("Debug[2]:%s"%lines[i],Enable)
                    #================================================================================
                    # [Level1]
                    else:
                        if  L1_ifdef==True and L1_else==False and L1_endif==False :
                            ###################################################################################
                            # <Level2>
                            if L2_ifdef==False and L2_else==False and L2_endif==False:

                                L2_MatchIf=False
                                if re.search(r"`ifdef",lines[i]):
                                    #ifdeflines=re.findall(r"`ifdef(.*?)\n", lines[i].replace(" ",""))
                                    for j in range(len(self.kfileToffile_define)):
                                        if ifdeflines==self.kfileToffile_define[j]:
                                            L2_MatchIf=True

                                    L2_if_store     =L2_MatchIf
                                    L2_else_store   =not L2_if_store#L2_MatchIf
                                    StoreInfo.append(False)
                                    L2_ifdef=True
                                    self.PrintLog("Debug[3]:%s"%lines[i],Enable)
                                else:
                                    if re.search(r"`else",lines[i]):
                                        L1_else=True

                                        L2_ifdef=False
                                        L2_else=False

                                        L2_if_store=False
                                        L2_else_store=False

                                        StoreInfo.append(False)
                                        self.PrintLog("Debug[4]:%s"%lines[i],Enable)
                                    else:
                                        if re.search(r"`endif",lines[i]):
                                            L1_ifdef=False
                                            L1_else=False

                                            L2_if_store=False
                                            L2_else_store=False

                                            StoreInfo.append(False)
                                            self.PrintLog("Debug[5]:%s"%lines[i],Enable)
                                        else:
                                            if L1_if_store==True:
                                                StoreInfo.append(True)
                                                self.PrintLog("Debug[5]:%s"%lines[i],Enable)
                                            else:
                                                StoreInfo.append(False)
                                                self.PrintLog("Debug[7]:%s"%lines[i],Enable)
                            ###################################################################################
                            # <Level2>
                            else:
                                if L2_ifdef==True and L2_else==False and L2_endif==False:

                                    if re.search(r"`else",lines[i]):
                                        L2_else=True
                                        StoreInfo.append(False)
                                        self.PrintLog("Debug[8]:%s"%lines[i],Enable)
                                    else:
                                        if re.search(r"`endif",lines[i]):
                                            L2_ifdef=False
                                            L2_else=False

                                            StoreInfo.append(False)
                                            self.PrintLog("Debug[9]:%s"%lines[i],Enable)
                                        else:
                                            if L1_if_store==True and L2_if_store==True:
                                                StoreInfo.append(True)
                                                self.PrintLog("Debug[10]:%s"%lines[i],Enable)
                                            else:
                                                StoreInfo.append(False)
                                                self.PrintLog("Debug[11]:%s"%lines[i],Enable)
                            ###################################################################################
                            # <Level2>
                                else:
                                    if L2_ifdef==True and L2_else==True and L2_endif==False:
                                        if re.search(r"`endif",lines[i]):
                                            L2_ifdef=False
                                            L2_else=False

                                            StoreInfo.append(False)
                                            self.PrintLog("Debug[12]:%s"%lines[i],Enable)
                                        else:
                                            if L1_if_store==True and L2_else_store==True:
                                                StoreInfo.append(True)
                                                self.PrintLog("Debug[13]:%s"%lines[i],Enable)
                                            else:
                                                StoreInfo.append(False)
                                                self.PrintLog("Debug[14]:%s"%lines[i],Enable)
                  
                        #================================================================================
                        else:
                            # [Level1]
                            if  L1_ifdef==True and L1_else==True and L1_endif==False :
                                ###################################################################################
                                # <Level2>
                                if L2_ifdef==False and L2_else==False and L2_endif==False:
                                    L2_MatchIf=False
                                    if re.search(r"`ifdef",lines[i]):
                                        #ifdeflines=re.findall(r"`ifdef(.*?)\n", lines[i].replace(" ",""))
                                        for j in range(len(self.kfileToffile_define)):
                                            if ifdeflines==self.kfileToffile_define[j]:
                                                L2_MatchIf=True

                                        L2_if_store     =L2_MatchIf
                                        L2_else_store   =not L2_if_store
                                        StoreInfo.append(False)
                                        L2_ifdef=True
                                        self.PrintLog("Debug[15]:%s"%lines[i],Enable)
                                    else:
                                        if re.search(r"`endif",lines[i]):
                                            L1_ifdef=False
                                            L1_else=False
                                            L2_if_store=False
                                            L2_else_store=False

                                            StoreInfo.append(False)
                                            self.PrintLog("Debug[16]:%s"%lines[i],Enable)
                                        else:
                                            if L1_else_store==True:
                                                StoreInfo.append(True)
                                                self.PrintLog("Debug[17]:%s"%lines[i],Enable)
                                            else:
                                                StoreInfo.append(False)
                                                self.PrintLog("Debug[18]:%s"%lines[i],Enable)
                                ###################################################################################
                                # <Level2>
                                else:
                                    if L2_ifdef==True and L2_else==False and L2_endif==False:

                                        if re.search(r"`else",lines[i]):
                                            L2_else=True
                                            StoreInfo.append(False)
                                            self.PrintLog("Debug[19]:%s"%lines[i],Enable)
                                        else:
                                            if re.search(r"`endif",lines[i]):
                                                L2_ifdef=False
                                                L2_else=False

                                                StoreInfo.append(False)
                                                self.PrintLog("Debug[20]:%s"%lines[i],Enable)
                                            else:
                                                if L1_else_store==True and L2_if_store==True:
                                                    StoreInfo.append(True)
                                                    self.PrintLog("Debug[21]:%s"%lines[i],Enable)
                                                else:
                                                    StoreInfo.append(False)
                                                    self.PrintLog("Debug[22]:%s"%lines[i],Enable)
                                ###################################################################################
                                # <Level2>
                                    else:
                                        if L2_ifdef==True and L2_else==True and L2_endif==False:
                                            if re.search(r"`endif",lines[i]):
                                                L2_ifdef=False
                                                L2_else=False

                                                StoreInfo.append(False)
                                                self.PrintLog("Debug[23]:%s"%lines[i],Enable)
                                            else:
                                                if L1_else_store==True and L2_else_store==True:
                                                    StoreInfo.append(True)
                                                    self.PrintLog("Debug[24]:%s"%lines[i],Enable)
                                                else:
                                                    StoreInfo.append(False)
                                                    self.PrintLog("Debug[25]:%s"%lines[i],Enable)

        #===========================================================================================
            #with open('%s'%filepath,'r',encoding='utf-8') as f:
            with open('%s'%filepath,'r') as f:
                lines=f.readlines()
                for i in range(len(StoreInfo)):
                    if StoreInfo[i]==True:
                        self.FileinfoAfterDefine.append(lines[i])
                    else:
                        self.FileinfoAfterDefine.append('')

        else:
            print("The path of file is not exist!!! Please ensure the path of the filename.k")


        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")
            print(len(StoreInfo))
            for i in range(len(StoreInfo)):
                print("[%s]%s:%s"%(i+1,StoreInfo[i],self.FileinfoAfterDefine[i]))
            print(self.kfileToffile_define)

    def PrintLog(self,str,Enable):
        if Enable==True:
            print("%s"%str)

if __name__ == '__main__':
    gen=gen_kf_ff()