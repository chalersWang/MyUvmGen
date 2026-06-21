#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os
import sys
import warnings
import shutil
from common_lib.parameters import Parameters
#warnings.filterwarnings("ignore")

script_path=os.path.split(os.path.realpath(__file__))[0]
print("[Script] : %s [Path]: %s"%(os.path.basename(__file__),script_path))
sys.path.append(script_path)

def PrintLog(self,str,Enable):
    if Enable==True:
        print("%s"%str)

def PrintArray(self,Array,PrintEnable):
    if PrintEnable==True:
        for i in range(len(Array)):
            print(Array[i])

def ExtractArray(self,sheetname,ExtractKeyword):
    ExtractKeywordName=[]
    for name in sheetname:
        if (not name.value ==None)&(not name.value==ExtractKeyword):
            ExtractKeywordName.append(name.value)
    return ExtractKeywordName

def getFileEnable(self,TitleName,FileName,Enable):
    for filename in TitleName:
        if filename.value == FileName:
            for EN in Enable:
                if EN.row == filename.row:
                    enable=EN.value
    return enable
    
def getVipNum(self,VIP_name,VipName,VipNum):
    for vipname in VIP_name:
        if vipname.value == VipName:
            for vipnum in VipNum:
                if vipnum.row == vipname.row:
                    Num=vipnum.value
    return Num

def CopyFile(self,SrcFile,DstFile):
    print("srcfile=%s"%SrcFile)
    print("dstfile=%s"%DstFile)
    if os.path.isfile(SrcFile):
        shutil.copy2(SrcFile, DstFile)
    else:
        warninfo(self)
        print(f"[{os.sys._getframe().f_code.co_name}] not been excuted!!!")

def DoScript(self,Script,CfgFile):
    py_exe = sys.executable
    if CfgFile==None:
        os.system("%s %s"%(py_exe, Script))
    else:
        os.system("%s %s %s"%(py_exe, Script, CfgFile))

def GetDirName(self,Path,Suffix):
    dir_name=[]
    if os.path.isdir(Path):
        flist=os.listdir(Path)
        for i in flist:
            if not os.path.splitext(i)[1]==Suffix:
                dir_name.append(i)
    else:
        warninfo(self)
        print(f"[{os.sys._getframe().f_code.co_name}] not been excuted!!!")
    
    return dir_name
    
def GetFileName(self,Path,Suffix):
    file_name=[]
    if os.path.isdir(Path):
        flist=os.listdir(Path)
        for i in flist:
            if os.path.splitext(i)[1]==Suffix:
                file_name.append(i)
    else:
        warninfo(self,Path)
        print(f"[{os.sys._getframe().f_code.co_name}] not been excuted!!!")

    if len(file_name)==0:
        warnings.warn("The file is not exist!")

    return file_name

def CreateDir(self,DirName):
    if not os.path.isdir(DirName):
        os.mkdir(DirName)
    else:
        warninfo(self,DirName)
        print(f"[{os.sys._getframe().f_code.co_name}] not been excuted!!!")

def CreateFileLink(self,Src,Dst):
    if os.path.isfile(Src):
        shutil.copy2(Src, Dst)
    else:
        warninfo(self,Src)
        print(f"[{os.sys._getframe().f_code.co_name}] not been excuted!!!")

def warninfo(self,Path):
    if os.path.isdir(Path):
        warnings.warn("The directory is not exist!!!")
        print("[%s]"%Path)

    elif os.path.isfile(Path):
        warnings.warn("The file is not exist!!!")
        print("[%s]"%Path)

def gen_uvm_new(self,filename,ObjectName,CompOrObject,StrStr,PrintEnable):
    if PrintEnable==True:
        print("[%s][new]:generation"%(filename.name))

    if CompOrObject=='uvm_component':
        filename.write("\tfunction new(string name=\"%s\",uvm_component parent=null);\n"%ObjectName)
        filename.write("\t\tsuper.new(name,parent);\n")
    elif CompOrObject=='uvm_object':
        filename.write("\tfunction new(string name=\"%s\");\n"%ObjectName)
        filename.write("\t\tsuper.new(name);\n")

    if StrStr!=None:
        filename.write("\t\t`uvm_info(get_full_name(),\"new() begin ...\",UVM_LOW)\n")
        for i in range(len(StrStr)):
            filename.write("\t\t%s\n"%StrStr[i])
        filename.write("\t\t`uvm_info(get_full_name(),\"new() end ...\",UVM_LOW)\n")
    else:
        filename.write("\t\t//`uvm_info(get_full_name(),\"new() begin ...\",UVM_LOW)\n")
        filename.write("\t\t//`uvm_info(get_full_name(),\"new() end ...\",UVM_LOW)\n")

    filename.write("\tendfunction\n")
    filename.write("\n")

def gen_uvm_phase(self,filename,PhaseName,StrStr,PrintEnable):
    if PrintEnable==True:
        print("[%s][%s]:generation"%(filename.name,PhaseName))
    
    if StrStr==None or StrStr==[]:
        filename.write("\t/*\n")
        
    filename.write("\t//%s\n"%PhaseName)
    if  PhaseName=='run_phase' or \
        PhaseName=='pre_reset_phase'        or PhaseName=='reset_phase'     or PhaseName=='post_reset_phase' or \
        PhaseName=='pre_configure_phase'    or PhaseName=='configure_phase' or PhaseName=='post_configure_phase' or \
        PhaseName=='pre_main_phase'         or PhaseName=='main_phase'      or PhaseName=='post_main_phase' or \
        PhaseName=='pre_shutdown_phase'     or PhaseName=='shutdown_phase'  or PhaseName=='post_shutdown_phase':
        
        filename.write("\tvirtual task %s(uvm_phase phase);\n"%PhaseName)
        filename.write("\t\tsuper.%s(phase);\n"%PhaseName)
        if StrStr!=None:
            filename.write("\t\t`uvm_info(get_full_name(),\"%s begin ...\",UVM_LOW)\n"%PhaseName)
            for i in range(len(StrStr)):
                filename.write("\t\t%s\n"%StrStr[i])
            filename.write("\t\t`uvm_info(get_full_name(),\"%s end ...\",UVM_LOW)\n"%PhaseName)
        else:
            filename.write("\t\t//`uvm_info(get_full_name(),\"%s begin ...\",UVM_LOW)\n"%PhaseName)
            filename.write("\t\t//`uvm_info(get_full_name(),\"%s end ...\",UVM_LOW)\n"%PhaseName)
        filename.write("\tendtask\n")
        filename.write("\n")
    else:
        filename.write("\tvirtual function void %s(uvm_phase phase);\n"%PhaseName)
        filename.write("\t\tsuper.%s(phase);\n"%PhaseName)
        if StrStr!=None:
            filename.write("\t\t`uvm_info(get_full_name(),\"%s begin ...\",UVM_LOW)\n"%PhaseName)
            for i in range(len(StrStr)):
                filename.write("\t\t%s\n"%StrStr[i])
            filename.write("\t\t`uvm_info(get_full_name(),\"%s end ...\",UVM_LOW)\n"%PhaseName)
        else:
            filename.write("\t\t//`uvm_info(get_full_name(),\"%s begin ...\",UVM_LOW)\n"%PhaseName)
            filename.write("\t\t//`uvm_info(get_full_name(),\"%s end ...\",UVM_LOW)\n"%PhaseName)
        filename.write("\tendfunction\n")

    if StrStr==None or StrStr==[]:
        filename.write("\t*/\n")
    filename.write("\n")

def gen_uvm_body(self,filename,ObjectName,StrStr,PrintEnable):
    if PrintEnable==True:
        print("[%s][%s]:generation"%(filename.name,ObjectName))

    filename.write("\tvirtual task %s();\n"%ObjectName)
    if StrStr!=None:
        filename.write("\t\t`uvm_info(get_full_name(),\"%s() begin ...\",UVM_LOW)\n"%ObjectName)
        for i in range(len(StrStr)):
            filename.write("\t\t%s\n"%StrStr[i])
        filename.write("\t\t`uvm_info(get_full_name(),\"%s end ...\",UVM_LOW)\n"%ObjectName)
    else:
        filename.write("\t\t//`uvm_info(get_full_name(),\"%s() begin ...\",UVM_LOW)\n"%ObjectName)
        filename.write("\t\t//`uvm_info(get_full_name(),\"%s end ...\",UVM_LOW)\n"%ObjectName)
    filename.write("\tendtask\n")
    filename.write("\n")

def GenVipAxiLibTask_Burst(self,File,ID,BURST,AddrWidth,DataWidth):
    File.write("\n")
    File.write("`ifdef VIP_AXI_%s_BURST%s\n"%(ID,BURST))
    File.write("\n")
    File.write("\ttask axi_write_%s_burst%s(input bit[%s-1:0]waddr,input bit[%s-1:0]wdata[%s]);\n"%(ID,BURST,AddrWidth,DataWidth,BURST))
    File.write("\t\t`uvm_do_on_with(axi_wr_seq,p_sequencer.axi_master_seqr_%s\n"%ID)
    File.write("\t\t\t{\n")
    File.write("\t\t\t\twirte_addr==waddr;\n")
    for i in range(0,BURST):
        File.write("\t\t\t\twrite_data[%s]==wdata[%s];\n"%(i,i))
    File.write("\t\t\t\tburst_len==%s;\n"%BURST)
    File.write("\t\t\t})\n")
    File.write("\tendtask\n")
    File.write("\n")
    File.write("\ttask axi_read_%s_burst%s(input bit[%s-1:0]raddr,input bit AutoCompare,input bit[%s-1:0]expdata[%s]);\n"%(ID,BURST,AddrWidth,DataWidth,BURST))
    File.write("\t\t`uvm_do_on_with(axi_rd_seq,p_sequencer.axi_master_seqr_%s\n"%ID)
    File.write("\t\t\t{\n")
    File.write("\t\t\t\tread_addr==raddr;\n")
    File.write("\t\t\t\tburst_len==%s;\n"%BURST)
    File.write("\t\t\t})\n")
    File.write("\n")
    File.write("\t\t%s_cfg.axi_rdata%s=new[%s];\n"%(self.tb_name,ID,BURST))
    File.write("\t\tforeach(axi_rd_seq.read_data[i])begin\n")
    File.write("\t\t\t%s_cfg.axi_rdata%s[%s]=axi_rd_seq.read_data[i];\n"%(self.tb_name,ID,BURST))
    File.write("\t\tend\n")
    File.write("\n")
    File.write("\t\tif(AutoCompare==1)begin\n")
    File.write("\t\t\tforeach(%s_cfg.axi_rdata%s[i])begin\n"%(self.tb_name,ID))
    File.write("\t\t\t\tif(%s_cfg.axi_rdata%s[i]!=expdata[i])begin\n"%(self.tb_name,ID))
    File.write("\t\t\t\t\t`uvm_error(\"axi read error\",$sformatf(\"\\nthe addr =%h\\nact_data=%h\\nexp_data=%h\\n\",\n")
    File.write("\t\t\t\t\t\t\traddr,%s_cfg.axi_rdata%s[i],expdata[i]))\n"%(self.tb_name,ID))
    File.write("\t\t\t\tend\n")
    File.write("\t\t\tend\n")
    File.write("\t\tend\n")
    File.write("\tendtask\n")
    File.write("\n")
    File.write("`endif\n")
    File.write("\n")

def GenVipAxiLibTask_NarrowBurst(self,File,ID,NBURST,AddrWidth,DataWidth):
    File.write("\n")
    File.write("`ifdef VIP_AXI_%s_NBURST\n"%ID)
    # write narrow burst
    File.write("\n")
    File.write("\ttask axi_write_%s_nburst(input bit[%s-1:0]waddr,input bit[%s-1:0]wdata,input[15:0]CfgBurst);\n"%(ID,AddrWidth,DataWidth))
    for i in range(len(NBURST)):
        if(i==0):
            File.write("\t\tif(CfgBurst==%s)begin\n"%NBURST[i])
        else:
            File.write("\t\telse if(CfgBurst==%s)begin\n"%NBURST[i])
        File.write("\t\t\t`uvm_do_on_with(axi_wr_nb_seq,p_sequencer.axi_master_seqr_%s\n"%ID),
        File.write("\t\t\t\t{\n")
        File.write("\t\t\t\t\twrite_addr   == waddr;\n")
        File.write("\t\t\t\t\twrite_data[0]== wdata;\n")
        File.write("\t\t\t\t\tburst_len    == 32'h1;\n")
        File.write("\t\t\t\t\tCfgBurst     == %s;\n"%NBURST[i])
        File.write("\t\t\t\t});\n")
        File.write("\t\tend\n")
    File.write("\n")
    File.write("\tendtask\n")
    File.write("\n")
    File.write("\n")
    File.write("\ttask axi_read_%s_nburst(input bit[%s-1:0]raddr,input bit AutoCompare,input bit[%s-1:0]exprdata,input[15:0]CfgBurst);\n"%(ID,AddrWidth,DataWidth))
    File.write("\t\tbit[%s-1:0]rdata;\n"%DataWidth)
    for i in range(len(NBURST)):
        if(i==0):
            File.write("\t\tif(CfgBurst==%s)begin\n"%NBURST[i])
        else:
            File.write("\t\telse if(CfgBurst==%s)begin\n"%NBURST[i])
        File.write("\t\t\t`uvm_do_on_with(axi_rd_nb_seq,p_sequencer.axi_master_seqr_%s\n"%ID),
        File.write("\t\t\t\t{\n")
        File.write("\t\t\t\t\tread_addr    == raddr;\n")
        File.write("\t\t\t\t\tburst_len    == 32'h1;\n")
        File.write("\t\t\t\t\tCfgBurst     == %s;\n"%NBURST[i])
        File.write("\t\t\t\t});\n")
        File.write("\t\tend\n")
    File.write("\n")
    File.write("\t\trdata=axi_rd_nb_seq.read_data[0];\n")
    File.write("\t\tif(AutoCompare==1)begin\n")
    File.write("\t\t\tif(rdata!=exprdata)begin\n")
    File.write("\t\t\t\t`uvm_error(\"axi narrow read error\",$sformatf(\"\\nthe addr=%0h\\nact_data=%0h\\nexp_data=%0h\",rdata,expdata))\n")
    File.write("\t\t\tend\n")
    File.write("\t\tend\n")
    File.write("\tendtask\n")
    File.write("\n")
    File.write("`endif\n")
    File.write("\n")

def GetDutSignalList(self,SIGNALS):
    Signals0=[]
    Signals1=[]
    Signals2=[]
    Signals3=[]
    Signals4=[]
    Signals5=[]
    Signals6=[]
    Signals7=[]
    Signals0=SIGNALS.replace('\n','')
    Signals1=Signals0.replace('input','')
    Signals2=Signals1.replace('output','')
    Signals2=Signals2.replace('inout','')
    Signals3=Signals2.replace(' ','')
    Signals4=Signals3.rstrip(',')
    Signals5=Signals4.split(',')
    #check signals X/Z
    for i in range(len(Signals5)):
        delaystrlst=Signals5[i][Signals5[i].find('['):Signals5[i].find(']')+1]
        if delaystrlst==None:
            Signals6=Signals5[i]
        else:
            Signals6=Signals5[i].replace(delaystrlst,'')
        Signals7.append(Signals6)
    return Signals7