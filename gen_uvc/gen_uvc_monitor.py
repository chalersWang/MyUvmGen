#! /usr/bin/env python
# -*-coding:UTF-8-*-
# ============================================================
# MyUvmGen_v2.0 — UVC Monitor 代码生成器
#
# 【设计说明】
# - run_phase 中统一采集所有 transaction，通过 analysis_port 广播
# - X/Z 检查独立于覆盖率收集，通过宏控制
# - 内建 monitor_callback，支持用户注册回调扩展 monitor 行为
# - 不再使用 forever fork join（会导致线程堆积），改为 forever 内串行处理
#
# 【UVM 方法论要点】
# - Monitor 应该始终采集数据（通过 analysis_port.write），
#   覆盖率收集在 scoreboard 或独立 subscriber 中完成
# - run_phase 适用于 monitor（因为监控在整个仿真期间都需要持续运行），
#   但 driver/sequencer 应使用 main_phase
# ============================================================
import os

from common_lib.parameters import Parameters
from common_lib.common_lib import gen_uvm_new
from common_lib.common_lib import gen_uvm_phase
from common_lib.common_lib import GetDutSignalList

class gen_uvc_monitor:

    def __init__(self):
        print("[gen_uvc_monitor]:initial")
        uvc_name='aa'
        uvc_signals=    "            \
                        input a     ,\
                        input[1:0]b ,\
                        output c    ,\
                        output[2:0]d,\
                        "
        self.gen_uvc_monitor_info(uvc_name,uvc_signals,PrintEnable=True)

    def gen_uvc_monitor_info(self,name,SIGNALS,PrintEnable):
        SignalList=GetDutSignalList(self,SIGNALS)
        
        filename = open("%s_monitor.sv"%name, "w+")
        filename.write("`ifndef _%s_MONITOR_SV_\n"%name.upper())
        filename.write("`define _%s_MONITOR_SV_\n"%name.upper())
        filename.write("\n")

        # ===== 类声明 =====
        filename.write("//=========================================================================\n")
        filename.write("// %s_monitor: 从接口采集 transaction，通过 analysis_port 广播\n"%name)
        filename.write("//   使用 run_phase 持续监控（监控类组件适合 run_phase，因其需全仿真期间运行）\n")
        filename.write("//   内建 monitor_callback 支持用户扩展\n")
        filename.write("//=========================================================================\n")
        filename.write("class %s_monitor extends uvm_monitor;\n"%name)
        filename.write("\n")
        filename.write("\tvirtual %s_vif       vif;\n"%name)
        filename.write("\t%s_trans             %s_tr;\n"%(name,name))
        filename.write("\n")
        filename.write("\tuvm_analysis_port #(%s_trans)    mon_analysis_port;\n"%name)
        filename.write("\t`uvm_register_cb(%s_monitor, %s_monitor_callback)\n"%(name,name))
        filename.write("\n")
        filename.write("\t`uvm_component_utils(%s_monitor)\n"%name)
        filename.write("\n")

        gen_uvm_new(self,filename,'%s_monitor'%name,'uvm_component',None,Parameters.PrintEnable)

        # build_phase
        StrStr=[]
        StrStr.append("mon_analysis_port=new(\"mon_analysis_port\",this);")
        gen_uvm_phase(self,filename,'build_phase',StrStr,Parameters.PrintEnable)

        # connect_phase: 获取 vif
        StrStr=[]
        StrStr.append("if(!uvm_config_db#(virtual %s_vif)::get(this,\"\",\"%s_vif\",vif))"%(name,name))
        StrStr.append("    `uvm_fatal(\"%s_monitor\",\"virtual interface must be set for it!!!\")"%name)
        gen_uvm_phase(self,filename,'connect_phase',StrStr,Parameters.PrintEnable)

        gen_uvm_phase(self,filename,'end_of_elaboration_phase',None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'start_of_simulation_phase',None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'reset_phase',None,Parameters.PrintEnable)

        # ===== run_phase: 持续监控（关键改进：不再 forever fork） =====
        filename.write("\t//=========================================================================\n")
        filename.write("\t// run_phase: 持续监控 DUT 信号，每个时钟周期采集一次 transaction\n")
        filename.write("\t//   X/Z 检查：通过 `ifdef CHECK_SIGNAL_XZ_%s 宏控制\n"%name.upper())
        filename.write("\t//   覆盖率采集：通过 `ifdef COVERAGE_%s 宏控制\n"%name.upper())
        filename.write("\t//   注意：原来使用 forever fork join，会导致每个时钟周期创建一个\n")
        filename.write("\t//   永不释放的线程，内存持续增长。已修复为串行 @(posedge vif.clk) 模式。\n")
        filename.write("\t//=========================================================================\n")
        filename.write("\tvirtual task run_phase(uvm_phase phase);\n")
        filename.write("\t\t`uvm_info(get_type_name(), \"run_phase begin\", UVM_MEDIUM)\n")
        filename.write("\n")
        filename.write("\t\tforever begin\n")
        filename.write("\n")
        filename.write("\t\t\t// --- 1. 等待时钟边沿（不再用 fork，避免线程泄漏） ---\n")
        filename.write("\t\t\t@(posedge vif.clk);\n")
        filename.write("\n")
        filename.write("\t\t\t// --- 2. X/Z 检查（通过宏控制，不影响正常采集） ---\n")
        filename.write("\t\t\t`ifdef CHECK_SIGNAL_XZ_%s\n"%name.upper())
        filename.write("\t\t\t\t// 检查所有信号是否存在 X 或 Z 状态\n")
        for i in range(len(SignalList)):
            filename.write("\t\t\t\tif($isunknown(vif.%s)==1)\n"%SignalList[i])
            filename.write("\t\t\t\t\t`uvm_error(get_type_name(), $sformatf(\"signal:%s is X/Z at %%0t\", $time))\n"%SignalList[i])
        filename.write("\t\t\t`endif\n")
        filename.write("\n")
        filename.write("\t\t\t// --- 3. 创建 transaction 并采样接口信号 ---\n")
        filename.write("\t\t\t%s_tr = %s_trans::type_id::create(\"%s_tr\");\n"%(name,name,name))
        for i in range(len(SignalList)):
            filename.write("\t\t\t%s_tr.%s = vif.%s;\n"%(name,SignalList[i],SignalList[i]))
        filename.write("\n")
        filename.write("\t\t\t// --- 4. 调用回调：pre_collect ---\n")
        filename.write("\t\t\t`uvm_do_callbacks(%s_monitor, %s_monitor_callback, pre_collect(this, %s_tr))\n"%(name,name,name))
        filename.write("\n")
        filename.write("\t\t\t// --- 5. 广播 transaction（始终执行，不依赖宏） ---\n")
        filename.write("\t\t\tmon_analysis_port.write(%s_tr);\n"%name)
        filename.write("\n")
        filename.write("\t\t\t// --- 6. 调用回调：post_collect ---\n")
        filename.write("\t\t\t`uvm_do_callbacks(%s_monitor, %s_monitor_callback, post_collect(this, %s_tr))\n"%(name,name,name))
        filename.write("\t\tend\n")
        filename.write("\t\t`uvm_info(get_type_name(), \"run_phase end\", UVM_MEDIUM)\n")
        filename.write("\tendtask : run_phase\n")
        filename.write("\n")

        gen_uvm_phase(self,filename,'extract_phase',None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'check_phase',None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'report_phase',None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'final_phase',None,Parameters.PrintEnable)

        filename.write("endclass : %s_monitor\n"%name)
        filename.write("\n")

        # ===== Callback 类定义 =====
        filename.write("\t//=========================================================================\n")
        filename.write("\t// %s_monitor_callback: Monitor 回调基类\n"%name)
        filename.write("\t//   用户可继承此类扩展 monitor 行为（如注入错误、修改采集数据等）\n")
        filename.write("\t//=========================================================================\n")
        filename.write("\tclass %s_monitor_callback extends uvm_callback;\n"%name)
        filename.write("\t\t`uvm_object_utils(%s_monitor_callback)\n"%name)
        filename.write("\t\tfunction new(string name=\"%s_monitor_callback\");\n"%name)
        filename.write("\t\t\tsuper.new(name);\n")
        filename.write("\t\tendfunction\n")
        filename.write("\n")
        filename.write("\t\t// 在 monitor 采样后、write 前调用，可修改 transaction\n")
        filename.write("\t\tvirtual function void pre_collect(%s_monitor mon, %s_trans tr);\n"%(name,name))
        filename.write("\t\tendfunction\n")
        filename.write("\n")
        filename.write("\t\t// 在 monitor write 后调用\n")
        filename.write("\t\tvirtual function void post_collect(%s_monitor mon, %s_trans tr);\n"%(name,name))
        filename.write("\t\tendfunction\n")
        filename.write("\tendclass : %s_monitor_callback\n"%name)
        filename.write("\n")

        filename.write("`endif\n")
        filename.close()

        if PrintEnable==True:
            print("[gen_uvc_monitor] %s_monitor.sv generated with:")
            print("  - fixed: removed forever fork (thread leak)")
            print("  - monitor always collects (not only under COVERAGE macro)")
            print("  - X/Z check under dedicated macro")
            print("  - monitor_callback for extensibility")

if __name__ == '__main__':
    gen=gen_uvc_monitor()
