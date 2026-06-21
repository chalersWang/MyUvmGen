#! /usr/bin/env python
# -*-coding:UTF-8-*-
# ============================================================
# MyUvmGen_v2.0 — Scoreboard 代码生成器
#
# 【设计说明】
# - 为每个 UVC 创建独立的 uvm_subscriber，处理比对逻辑
# - 覆盖率收集从 scoreboard 中分离，通过独立的 coverage subscriber 完成
# - scoreboard 接收所有 monitor 的 analysis_port 输出，集中比对
# - 使用 phase 同步（等待复位释放后才开始处理）
#
# 【UVM 方法论要点】
# - uvm_subscriber: TLM analysis port 的标准消费者，
#   自动处理 analysis_fifo 的 get/peek 逻辑
# - 比对和覆盖率是两个独立关注点，应分离：
#   比对 → scoreboard / reference model
#   覆盖率 → coverage collector (独立 subscriber)
# - 解耦后每个组件职责单一，方便复用和测试
# ============================================================
import os
from common_lib.parameters import Parameters
from common_lib.common_lib import gen_uvm_new
from common_lib.common_lib import gen_uvm_phase
from common_lib.common_lib import gen_uvm_body

class gen_env_scoreboard:

    def __init__(self):
        print("[gen_env_scoreboard]:initial")
        self.gen_env_scoreboard_info(PrintEnable=True)

    def gen_env_scoreboard_info(self,PrintEnable):
        filename = open("%s_scoreboard.sv"%self.tb_name, "w+")
        filename.write("`ifndef _%s_SCOREBOARD_SV_\n"%self.tb_name.upper())
        filename.write("`define _%s_SCOREBOARD_SV_\n"%self.tb_name.upper())
        filename.write("\n")

        filename.write("//=========================================================================\n")
        filename.write("// %s_scoreboard: 验证环境计分板\n"%self.tb_name)
        filename.write("//   职责：接收 monitor 的 transaction，比对期望值与实际值\n")
        filename.write("//   覆盖率收集已独立为 coverage_subscriber（见 %s_function_coverage.sv）\n"%self.tb_name)
        filename.write("//=========================================================================\n")
        
        # Include coverage
        if self.tb_name:
            filename.write("`include \"%s_function_coverage.sv\"\n"%self.tb_name)
        filename.write("\n")
        filename.write("class %s_scoreboard extends uvm_scoreboard;\n"%self.tb_name)
        filename.write("\n")
        filename.write("\t// 配置和事件\n")
        filename.write("\t%s_config   %s_cfg;\n"%(self.tb_name, self.tb_name))
        filename.write("\n")
        
        # 为每个 UVC 创建 subscriber 和 analysis_imp
        uvc_count = 0
        filename.write("\t// ===== UVC Subscriber 声明 =====\n")
        filename.write("\t// 每个 UVC 一个 subscriber，接收其 monitor 的 transaction\n")
        for i in range(len(self.DUT_GroupName)):
            if self.DUT_VIP[i]==False:
                uvc_count += 1
                filename.write("\tuvm_analysis_imp_%s #(%s_trans, %s_scoreboard) %s_scb_imp;\n"%(
                    self.DUT_GroupName[i], self.DUT_GroupName[i], self.tb_name, self.DUT_GroupName[i]))
        # VIP also has analysis port
        for vip_name in self.VIP_DB.keys():
            if self.VIP_DB[vip_name]['Enable']:
                uvc_count += 1
        
        filename.write("\n")
        filename.write("\t`uvm_component_utils(%s_scoreboard)\n"%self.tb_name)
        filename.write("\n")

        gen_uvm_new(self,filename,'%s_scoreboard'%self.tb_name,'uvm_component',None,Parameters.PrintEnable)

        # build_phase
        StrStr=[]
        for i in range(len(self.DUT_GroupName)):
            if self.DUT_VIP[i]==False:
                StrStr.append("%s_scb_imp = new(\"%s_scb_imp\", this);"%(
                    self.DUT_GroupName[i], self.DUT_GroupName[i]))
        gen_uvm_phase(self,filename,'build_phase',StrStr,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'connect_phase',None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'end_of_elaboration_phase',None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'start_of_simulation_phase',None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'reset_phase',None,Parameters.PrintEnable)

        # run_phase: 获取 config
        StrStr=[]
        StrStr.append("// 等待复位释放")
        StrStr.append("@(posedge %s_vif.rstn);" % self.tb_name)  # 近似，实际情况由 tb_name_vif 提供
        StrStr.append("")
        StrStr.append("// 获取 config")
        StrStr.append("if(!uvm_config_db#(%s_config)::get(this, \"\", \"%s_config\", %s_cfg))"%(
            self.tb_name, self.tb_name, self.tb_name))
        StrStr.append("    `uvm_error(get_type_name(), \"failed to get config\")")
        gen_uvm_phase(self,filename,'run_phase',StrStr,Parameters.PrintEnable)

        # ===== write 方法：每个 UVC 一个 =====
        for i in range(len(self.DUT_GroupName)):
            if self.DUT_VIP[i]==False:
                filename.write("\n")
                filename.write("\t// %s 数据比对（由 %s_scb_imp 回调）\n"%(self.DUT_GroupName[i], self.DUT_GroupName[i]))
                filename.write("\tfunction void write_%s(%s_trans tr);\n"%(self.DUT_GroupName[i], self.DUT_GroupName[i]))
                filename.write("\t\t`uvm_info(get_type_name(), $sformatf(\"%s rcv trans: %%s\", tr.convert2string()), UVM_HIGH)\n"%self.DUT_GroupName[i])
                filename.write("\t\t// TODO: 用户在此实现 %s 的比对逻辑\n"%self.DUT_GroupName[i])
                filename.write("\t\t// 典型比对流程：\n")
                filename.write("\t\t//   1. 从 reference model 获取期望值\n")
                filename.write("\t\t//   2. 与 monitor 采集的实际值比对\n")
                filename.write("\t\t//   3. 不匹配时报告 `uvm_error\n")
                filename.write("\tendfunction : write_%s\n"%self.DUT_GroupName[i])

        gen_uvm_phase(self,filename,'extract_phase',None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'check_phase',None,Parameters.PrintEnable)
        
        # report_phase: 统计结果
        StrStr=[]
        StrStr.append("`uvm_info(get_type_name(), $sformatf(\"scoreboard report:\"), UVM_LOW)")
        StrStr.append("// TODO: 打印比对统计（pass/fail 计数）")
        gen_uvm_phase(self,filename,'report_phase',StrStr,Parameters.PrintEnable)
        
        gen_uvm_phase(self,filename,'final_phase',None,Parameters.PrintEnable)

        filename.write("endclass : %s_scoreboard\n"%self.tb_name)
        filename.write("\n")
        filename.write("`endif\n")
        filename.close()

        if PrintEnable==True:
            print("[gen_env_scoreboard] %s_scoreboard.sv generated with:"%self.tb_name)
            print("  - one uvm_analysis_imp per UVC (decoupled)")
            print("  - coverage separated to function_coverage.sv")
            print("  - per-UVC write_%s method for comparison logic"%"<name>")

if __name__ == '__main__':
    gen=gen_env_scoreboard()
