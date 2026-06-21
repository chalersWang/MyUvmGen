#! /usr/bin/env python
# import binascii
# -*-coding:UTF-8-*-
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# from readexcel.readexcel_WorkingDirectoryGen import readexcel_WorkingDirectoryGen
# from readexcel.readexcel_VIP import readexcel_VIP
from readexcel.readexcel_DutSignal import readexcel_DutSignal
# from readexcel.readexcel_ClockRst import readexcel_ClockRst
from common_lib.parameters import Parameters
from common_lib.common_lib import gen_uvm_new
from common_lib.common_lib import gen_uvm_phase
from common_lib.common_lib import gen_uvm_body

class gen_testcase_demo_test:

    def __init__(self):
        print("[gen_testcase_demo_test]:initial")
        #EnvironmentGenCfg='../VerifyEnvironmentGenCfg.xlsx'
        EnvironmentGenCfg=Parameters.EnvironmentGenCfg
        # readexcel_WorkingDirectoryGen.readexcel_WorkingDirectoryGen_info(self,EnvironmentGenCfg,PrintEnable=False)
        # readexcel_VIP.readexcel_VIP_info(self,EnvironmentGenCfg,PrintEnable=False)
        # readexcel_ClockRst.readexcel_ClockRst_info(self,EnvironmentGenCfg,PrintEnable=False)
        readexcel_DutSignal.readexcel_DutSignal_info(self,EnvironmentGenCfg,PrintEnable=False)
        self.gen_testcase_demo_test_info(Parameters.tb_name,PrintEnable=True)

    def gen_testcase_demo_test_info(self,name,PrintEnable):
        filename = open("%s_demo_test.sv"%name, "w+")
        filename.write("`ifndef _%s_DEMO_TEST_SV_\n"%name.upper())
        filename.write("`define _%s_DEMO_TEST_SV_\n"%name.upper())
        ############################################################################################################
        filename.write("\n")
        for i in range(len(self.DUT_GroupName)):
            if self.DUT_VIP[i]==True:filename.write("`ifndef NO_%s_CUSTOM\n"%self.DUT_GroupName[i])            
            filename.write("class %s_demo_%s_sequence extends %s_sequence_lib;\n"%(name,self.DUT_GroupName[i],self.DUT_GroupName[i]))
            filename.write("\n")
            filename.write("    integer status;\n")
            filename.write("\n")
            filename.write("    `uvm_object_utils(%s_demo_%s_sequence)\n"%(name,self.DUT_GroupName[i]))
            filename.write("\n")
            gen_uvm_new(self,filename,'%s_demo_%s_sequence'%(name,self.DUT_GroupName[i]),'uvm_object',None,Parameters.PrintEnable)
            StrStr=[]
            StrStr.append("     `uvm_create(tr)")
            StrStr.append("     //status=tr.randomize();")
            StrStr.append("     status=tr.randomize with{};")
            StrStr.append("     if(!status)`uvm_fatal(get_full_name,\"Can't randomize a trans!!!\")")
            StrStr.append("     `uvm_send(tr)")
            StrStr.append("     //tr.print();")
            StrStr.append("     //get_response(rsp);")
            gen_uvm_body(self,filename,'body'               ,StrStr,Parameters.PrintEnable)
            if self.DUT_VIP[i]==True:filename.write("`endif\n")
            filename.write("endclass\n")
            filename.write("\n")
        ############################################################################################################        
        filename.write("\n")
        filename.write("class %s_demo_sequence extends %s_virtual_seq_lib;\n"%(name,name))
        filename.write("\n")
        for i in range(len(self.DUT_GroupName)):
            if self.DUT_VIP[i]==True:filename.write("    `ifndef NO_%s_CUSTOM\n"%self.DUT_GroupName[i])
            filename.write("    %s_demo_%s_sequence     %s_demo_%s_seq;\n"%(name,self.DUT_GroupName[i],name,self.DUT_GroupName[i]))
            if self.DUT_VIP[i]==True:filename.write("    `endif\n")
        filename.write("\n")
        filename.write("\t`uvm_object_utils(%s_demo_sequence)\n"%name)
        filename.write("\n")
        StrStr=[]
        for i in range(len(self.DUT_GroupName)):
            if self.DUT_VIP[i]==True:StrStr.append("\t`ifndef NO_%s_CUSTOM"%self.DUT_GroupName[i])
            StrStr.append("\t%s_demo_%s_seq=%s_demo_%s_sequence::type_id::create(\"%s_demo_%s_seq\");"
                        %(name,self.DUT_GroupName[i],name,self.DUT_GroupName[i],name,self.DUT_GroupName[i]))
            if self.DUT_VIP[i]==True:StrStr.append("\t`endif")
        gen_uvm_new(self,filename,'%s_demo_sequence'%name,'uvm_object',StrStr,Parameters.PrintEnable)
        # filename.write("\n")
        # filename.write("\tvirtual task body();\n")
        # filename.write("\t\t`uvm_info(get_full_name(),\"body\",UVM_LOW)\n")
        # filename.write("\t\t//add your transaction or sequence_lib\n")
        # filename.write("\tendtask\n")
        StrStr=[]
        StrStr.append("\t//add your transaction or sequence_lib")
        StrStr.append("\tfork")
        for i in range(len(self.DUT_GroupName)):
            if self.DUT_VIP[i]==True:StrStr.append("\t\t`ifndef NO_%s_CUSTOM"%self.DUT_GroupName[i])
            StrStr.append("\t\tbegin")
            StrStr.append("\t\t   %s_demo_%s_seq.start(p_sequencer.%s_seqr);"%(name,self.DUT_GroupName[i],self.DUT_GroupName[i]))
            StrStr.append("\t\tend")
            if self.DUT_VIP[i]==True:StrStr.append("\t\t`endif")
        StrStr.append("\tjoin")
        gen_uvm_body(self,filename,'body'               ,StrStr,Parameters.PrintEnable)
        filename.write("endclass\n")
        filename.write("\n")
        ############################################################################################################
        filename.write("class %s_demo_test extends %s_base_test;\n"%(name,name))
        filename.write("\n")
        filename.write("\t%s_demo_sequence  %s_demo_seq;\n"%(name,name))
        filename.write("\n")
        filename.write("\t`uvm_component_utils(%s_demo_test)\n"%name)
        filename.write("\n")
        StrStr=[]
        StrStr.append("%s_demo_seq=%s_demo_sequence::type_id::create(\"%s_demo_seq\");"%(name,name,name))
        gen_uvm_new(self,filename,'%s_demo_test'%name,'uvm_component',StrStr,Parameters.PrintEnable)
        # gen_uvm_phase(self,filename,'build_phase'               ,StrStr,Parameters.PrintEnable)
        # gen_uvm_phase(self,filename,'connect_phase'             ,None,Parameters.PrintEnable)
        # gen_uvm_phase(self,filename,'end_of_elaboration_phase'  ,None,Parameters.PrintEnable)
        # gen_uvm_phase(self,filename,'start_of_simulation_phase' ,None,Parameters.PrintEnable)
        StrStr=[]
        StrStr.append("phase.raise_objection(this);")
        StrStr.append("@(posedge %svif.rstn);"%name)
        StrStr.append("%s_demo_seq.start(env.%s_vseqr);"%(name,name))
        StrStr.append("#1us;")
        StrStr.append("phase.drop_objection(this);")
        gen_uvm_phase(self,filename,'run_phase'                 ,StrStr,Parameters.PrintEnable)
        # gen_uvm_phase(self,filename,'main_phase'                ,None,Parameters.PrintEnable)
        # gen_uvm_phase(self,filename,'extract_phase'             ,None,Parameters.PrintEnable)
        # gen_uvm_phase(self,filename,'check_phase'               ,None,Parameters.PrintEnable)
        # gen_uvm_phase(self,filename,'report_phase'              ,None,Parameters.PrintEnable)
        # gen_uvm_phase(self,filename,'final_phase'               ,None,Parameters.PrintEnable)
        filename.write("endclass\n")
        filename.write("\n")
        filename.write("`endif\n")
        filename.close()

        if PrintEnable==True:
            print("Please define the infomation of printing that you need!!!")
            
if __name__ == '__main__':
    gen=gen_testcase_demo_test()