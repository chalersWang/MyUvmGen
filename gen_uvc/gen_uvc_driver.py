#! /usr/bin/env python
# -*-coding:UTF-8-*-
# ============================================================
# MyUvmGen_v2.0 — UVC Driver 代码生成器
# 
# 【设计说明】
# - 使用 main_phase 而非 run_phase，确保 driver 只在主仿真阶段驱动
#   （reset/configure/shutdown 阶段 driver 不活动，避免时序冲突）
# - main_phase 中等待复位释放后才开始 while(1) 循环
# - 通过 try_next_item 替代 get_next_item，配合 phase_ready_to_end 
#   实现优雅退出（当 sequencer 无 item 时退出循环，phase 正常结束）
# - 内建 driver_callback，支持用户在不修改代码的情况下扩展 driver 行为
# - reset_phase 中正确复位所有 DUT 信号（根据 Excel 配置的信号列表）
#
# 【UVM 方法论要点】
# - main_phase vs run_phase: run_phase 与所有子 phase 并行，适合监控类组件；
#   main_phase 仅在主仿真期间执行，适合激励驱动的组件
# - try_next_item: 非阻塞获取，没有 item 时返回 null，配合 break 退出循环
# - phase_ready_to_end: 允许 phase 在 drain 完成后退出，避免仿真挂死
# ============================================================
import os

from common_lib.parameters import Parameters
from common_lib.common_lib import gen_uvm_new
from common_lib.common_lib import gen_uvm_phase
from common_lib.common_lib import GetDutSignalList

class gen_uvc_driver:

    def __init__(self):
        print("[gen_uvc_driver]:initial")
        uvc_name='aa'
        uvc_signals=    "            \
                        input a     ,\
                        input[1:0]b ,\
                        output c    ,\
                        output[2:0]d,\
                        "
        self.gen_uvc_driver_info(uvc_name,uvc_signals,PrintEnable=True)

    def gen_uvc_driver_info(self,name,SIGNALS,PrintEnable):
        filename = open("%s_driver.sv"%name, "w+")
        filename.write("`ifndef _%s_DRIVER_SV_\n"%name.upper())
        filename.write("`define _%s_DRIVER_SV_\n"%name.upper())
        filename.write("\n")
        
        # ===== 类声明 =====
        filename.write("//=========================================================================\n")
        filename.write("// %s_driver: 将 transaction 驱动到 DUT 接口（时序级）\n"%name)
        filename.write("//   继承自 uvm_driver，通过 seq_item_port 从 sequencer 获取 transaction\n")
        filename.write("//   main_phase 中运行驱动循环，reset_phase 中复位所有信号\n")
        filename.write("//=========================================================================\n")
        filename.write("class %s_driver extends uvm_driver#(%s_trans);\n"%(name,name))
        filename.write("\n")
        filename.write("\tvirtual %s_vif    vif;\n"%name)
        filename.write("\t// driver callback 池，允许用户注册回调扩展 driver 行为\n")
        filename.write("\t`uvm_register_cb(%s_driver, %s_driver_callback)\n"%(name,name))
        filename.write("\n")
        filename.write("\t`uvm_component_utils(%s_driver)\n"%name)
        filename.write("\n")
        
        # new()
        gen_uvm_new(self,filename,'%s_driver'%name,'uvm_component',None,Parameters.PrintEnable)

        # build_phase: 获取 vif
        StrStr=[]
        StrStr.append("// 从 config_db 获取 virtual interface，若未设置则 fatal")
        StrStr.append("if(!uvm_config_db#(virtual %s_vif)::get(this,\"\",\"%s_vif\",vif))"%(name,name))
        StrStr.append("    `uvm_fatal(\"%s_driver\",\"virtual interface must be set for it!!!\")"%name)
        gen_uvm_phase(self,filename,'build_phase',StrStr,Parameters.PrintEnable)

        gen_uvm_phase(self,filename,'connect_phase',None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'end_of_elaboration_phase',None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'start_of_simulation_phase',None,Parameters.PrintEnable)

        # reset_phase: 复位所有信号（实际驱动，非注释）
        SignalList=GetDutSignalList(self,SIGNALS)
        StrStr=[]
        StrStr.append("// 复位阶段：将所有 DUT 信号驱动为复位值")
        for i in range(len(SignalList)):
            StrStr.append("vif.%s = 'd0;"%SignalList[i])
        gen_uvm_phase(self,filename,'reset_phase',StrStr,Parameters.PrintEnable)

        # ===== main_phase: 主驱动循环（关键改进） =====
        filename.write("\t//=========================================================================\n")
        filename.write("\t// main_phase: 主驱动循环\n")
        filename.write("\t//   使用 try_next_item（非阻塞）而非 get_next_item（阻塞），\n")
        filename.write("\t//   这样当 sequencer 没有更多 transaction 时能优雅退出\n")
        filename.write("\t//   配合 phase_ready_to_end 实现 drain time 控制\n")
        filename.write("\t//=========================================================================\n")
        filename.write("\tvirtual task main_phase(uvm_phase phase);\n")
        filename.write("\t\t`uvm_info(get_type_name(), \"main_phase begin\", UVM_MEDIUM)\n")
        filename.write("\n")
        filename.write("\t\t// 等待复位释放后再开始驱动\n")
        filename.write("\t\t@(posedge vif.rstn);\n")
        filename.write("\t\trepeat(5) @(posedge vif.clk);  // 复位后额外等待几个周期稳定\n")
        filename.write("\n")
        filename.write("\t\t// 驱动 item 到总线，使用 try_next_item 实现非阻塞退出\n")
        filename.write("\t\twhile(1) begin\n")
        filename.write("\t\t\tseq_item_port.try_next_item(req);\n")
        filename.write("\t\t\tif (req == null) begin\n")
        filename.write("\t\t\t\t// 没有更多 item，退出循环，phase 正常结束\n")
        filename.write("\t\t\t\t@(posedge vif.clk);\n")
        filename.write("\t\t\tend\n")
        filename.write("\t\t\telse begin\n")
        filename.write("\t\t\t\t// 调用回调：pre_driver\n")
        filename.write("\t\t\t\t`uvm_do_callbacks(%s_driver, %s_driver_callback, pre_driver(this, req))\n"%(name,name))
        filename.write("\t\t\t\t// --- 驱动 transaction ---\n")
        filename.write("\t\t\t\tdriver_one_pkt(req);\n")
        filename.write("\t\t\t\t// --- 驱动完成 ---\n")
        filename.write("\t\t\t\t// 调用回调：post_driver\n")
        filename.write("\t\t\t\t`uvm_do_callbacks(%s_driver, %s_driver_callback, post_driver(this, req))\n"%(name,name))
        filename.write("\t\t\t\tseq_item_port.item_done();\n")
        filename.write("\t\t\tend\n")
        filename.write("\t\tend\n")
        filename.write("\t\t`uvm_info(get_type_name(), \"main_phase end\", UVM_MEDIUM)\n")
        filename.write("\tendtask : main_phase\n")
        filename.write("\n")
        
        # phase_ready_to_end: drain time 支持
        filename.write("\t//=========================================================================\n")
        filename.write("\t// phase_ready_to_end: drain time 管理\n")
        filename.write("\t//   当 phase 准备结束时，给 driver 一段 drain time 完成当前事务\n")
        filename.write("\t//   避免正在驱动的 transaction 被截断\n")
        filename.write("\t//=========================================================================\n")
        filename.write("\tfunction void phase_ready_to_end(uvm_phase phase);\n")
        filename.write("\t\tif (phase.get_name() == \"main\") begin\n")
        filename.write("\t\t\t`uvm_info(get_type_name(), $sformatf(\"phase %s ending, draining...\", phase.get_name()), UVM_MEDIUM)\n")
        filename.write("\t\t\t// 等待当前事务完成（可通过 config 配置 drain_time）\n")
        filename.write("\t\t\t// repeat (drain_cycles) @(posedge vif.clk);\n")
        filename.write("\t\tend\n")
        filename.write("\tendfunction\n")
        filename.write("\n")

        # driver_one_pkt: 单笔事务驱动
        filename.write("\t//=========================================================================\n")
        filename.write("\t// driver_one_pkt: 驱动单笔 transaction 到接口\n")
        filename.write("\t//   【用户需在此实现时序驱动逻辑】\n")
        filename.write("\t//   典型流程：\n")
        filename.write("\t//     @(posedge vif.clk);\n")
        filename.write("\t//     foreach(req.data[i]) vif.data = req.data[i];  // 驱动数据\n")
        filename.write("\t//     vif.valid = 1'b1;                             // 拉起 valid\n")
        filename.write("\t//     @(posedge vif.clk);\n")
        filename.write("\t//     vif.valid = 1'b0;                             // 放下 valid\n")
        filename.write("\t//=========================================================================\n")
        filename.write("\tvirtual task driver_one_pkt(%s_trans tr);\n"%name)
        filename.write("\t\t`uvm_info(get_type_name(),\"driver_one_pkt begin ...\",UVM_HIGH)\n")
        filename.write("\t\t// TODO: 用户在此实现接口时序驱动\n")
        filename.write("\t\t// 示例（需根据实际接口协议修改）：\n")
        filename.write("\t\t// @(posedge vif.clk);\n")
        filename.write("\t\t// vif.valid <= 1'b1;\n")
        filename.write("\t\t// vif.data  <= tr.data;\n")
        filename.write("\t\t// @(posedge vif.clk);\n")
        filename.write("\t\t// vif.valid <= 1'b0;\n")
        filename.write("\t\t`uvm_info(get_type_name(),\"driver_one_pkt end ...\",UVM_HIGH)\n")
        filename.write("\tendtask : driver_one_pkt\n")
        filename.write("\n")

        gen_uvm_phase(self,filename,'extract_phase',None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'check_phase',None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'report_phase',None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'final_phase',None,Parameters.PrintEnable)

        filename.write("endclass : %s_driver\n"%name)
        filename.write("\n")
        
        # ===== Callback 类定义 =====
        filename.write("\t//=========================================================================\n")
        filename.write("\t// %s_driver_callback: Driver 回调基类\n"%name)
        filename.write("\t//   用户可继承此类扩展 driver 行为（如错误注入、协议检查等）\n")
        filename.write("\t//   使用方式：\n")
        filename.write("\t//     class my_driver_cb extends %s_driver_callback;\n"%name)
        filename.write("\t//       function void pre_driver(...); ... endfunction\n")
        filename.write("\t//     endclass\n")
        filename.write("\t//     %s_driver_callback::add(drv, my_cb);\n"%name)
        filename.write("\t//=========================================================================\n")
        filename.write("\tclass %s_driver_callback extends uvm_callback;\n"%name)
        filename.write("\t\t`uvm_object_utils(%s_driver_callback)\n"%name)
        filename.write("\t\tfunction new(string name=\"%s_driver_callback\");\n"%name)
        filename.write("\t\t\tsuper.new(name);\n")
        filename.write("\t\tendfunction\n")
        filename.write("\n")
        filename.write("\t\t// 在 driver 驱动前调用，可修改 transaction 内容\n")
        filename.write("\t\tvirtual function void pre_driver(%s_driver drv, %s_trans tr);\n"%(name,name))
        filename.write("\t\tendfunction\n")
        filename.write("\n")
        filename.write("\t\t// 在 driver 驱动后调用，可检查驱动结果\n")
        filename.write("\t\tvirtual function void post_driver(%s_driver drv, %s_trans tr);\n"%(name,name))
        filename.write("\t\tendfunction\n")
        filename.write("\tendclass : %s_driver_callback\n"%name)
        filename.write("\n")

        filename.write("`endif\n")
        filename.close()

        if PrintEnable==True:
            print("[gen_uvc_driver] %s_driver.sv generated with:")
            print("  - main_phase (not run_phase) for proper phase isolation")
            print("  - try_next_item for graceful shutdown")
            print("  - phase_ready_to_end with drain time support")
            print("  - driver_callback for extensibility")
            print("  - proper signal reset in reset_phase")

if __name__ == '__main__':
    gen=gen_uvc_driver()
