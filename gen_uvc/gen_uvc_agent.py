#! /usr/bin/env python
# -*-coding:UTF-8-*-
# ============================================================
# MyUvmGen_v2.0 — UVC Agent 代码生成器
#
# 【设计说明】
# - 支持 UVM_ACTIVE / UVM_PASSIVE 双模式
#   - UVM_ACTIVE: 例化 driver + sequencer + monitor（可驱动总线）
#   - UVM_PASSIVE: 仅例化 monitor（纯监控，用于 slave/reference model 侧）
# - build_phase 根据 is_active 条件创建组件
# - connect_phase 连接 driver ↔ sequencer 的 TLM 端口
# - 内建 agent_callback，支持注入 agent 级行为
#
# 【UVM 方法论要点】
# - is_active 通过 uvm_config_db 从上层传入（env 或 test），
#   实现编译时组件的灵活配置
# - agent 是最佳的回调注册点：既能看到 driver 也能看到 monitor
# ============================================================
import os

from common_lib.parameters import Parameters
from common_lib.common_lib import gen_uvm_new
from common_lib.common_lib import gen_uvm_phase

class gen_uvc_agent:

    def __init__(self):
        print("[gen_uvc_agent]:initial")
        self.gen_uvc_agent_info(name='xx',PrintEnable=True)

    def gen_uvc_agent_info(self,name,PrintEnable):
        filename = open("%s_agent.sv"%name, "w+")
        filename.write("`ifndef _%s_AGENT_SV_\n"%name.upper())
        filename.write("`define _%s_AGENT_SV_\n"%name.upper())
        filename.write("\n")

        filename.write("//=========================================================================\n")
        filename.write("// %s_agent: %s UVC 的顶层 agent\n"%(name, name))
        filename.write("//   UVM_ACTIVE: 例化 driver + sequencer + monitor\n")
        filename.write("//   UVM_PASSIVE: 仅例化 monitor\n")
        filename.write("//   内建 agent_callback，支持 agent 级扩展\n")
        filename.write("//=========================================================================\n")
        filename.write("class %s_agent extends uvm_agent;\n"%name)
        filename.write("\n")
        filename.write("\t// is_active 控制 agent 工作模式（active=可驱动，passive=纯监控）\n")
        filename.write("\tuvm_active_passive_enum is_active = UVM_ACTIVE;\n")
        filename.write("\n")
        filename.write("\t// 子组件句柄\n")
        filename.write("\t%s_driver    %s_drv;\n"%(name,name))
        filename.write("\t%s_sequencer %s_seqr;\n"%(name,name))
        filename.write("\t%s_monitor   %s_mon;\n"%(name,name))
        filename.write("\n")
        filename.write("\t// agent callback 池（供用户注册扩展）\n")
        filename.write("\t`uvm_register_cb(%s_agent, %s_agent_callback)\n"%(name,name))
        filename.write("\n")
        filename.write("\t`uvm_component_utils_begin(%s_agent)\n"%name)
        filename.write("\t\t`uvm_field_enum(uvm_active_passive_enum, is_active, UVM_ALL_ON)\n")
        filename.write("\t\t`uvm_field_object(%s_drv,  UVM_ALL_ON)\n"%name)
        filename.write("\t\t`uvm_field_object(%s_mon,  UVM_ALL_ON)\n"%name)
        filename.write("\t\t`uvm_field_object(%s_seqr, UVM_ALL_ON)\n"%name)
        filename.write("\t`uvm_component_utils_end\n")
        filename.write("\n")

        gen_uvm_new(self,filename,'%s_agent'%name,'uvm_component',None,Parameters.PrintEnable)

        # build_phase
        StrStr=[]
        StrStr.append("// 从 config_db 获取 is_active（可由 env/test 通过 config_db 覆盖）")
        StrStr.append("uvm_config_db#(uvm_active_passive_enum)::get(this,\"\",\"is_active\",is_active);")
        StrStr.append("if(is_active==UVM_ACTIVE)begin")
        StrStr.append("    %s_drv  = %s_driver::type_id::create(\"%s_drv\", this);"%(name,name,name))
        StrStr.append("    %s_seqr = %s_sequencer::type_id::create(\"%s_seqr\", this);"%(name,name,name))
        StrStr.append("end")
        StrStr.append("%s_mon = %s_monitor::type_id::create(\"%s_mon\", this);"%(name,name,name))
        gen_uvm_phase(self,filename,'build_phase',StrStr,Parameters.PrintEnable)

        # connect_phase
        StrStr=[]
        StrStr.append("// 仅在 ACTIVE 模式连接 driver ↔ sequencer 的 TLM 端口")
        StrStr.append("if(is_active==UVM_ACTIVE)begin")
        StrStr.append("    %s_drv.seq_item_port.connect(%s_seqr.seq_item_export);"%(name,name))
        StrStr.append("    // rsp_port 用于 driver→sequencer 的响应回传")
        StrStr.append("    %s_drv.rsp_port.connect(%s_seqr.rsp_export);"%(name,name))
        StrStr.append("end")
        gen_uvm_phase(self,filename,'connect_phase',StrStr,Parameters.PrintEnable)

        gen_uvm_phase(self,filename,'end_of_elaboration_phase',None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'start_of_simulation_phase',None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'run_phase',None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'extract_phase',None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'check_phase',None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'report_phase',None,Parameters.PrintEnable)
        gen_uvm_phase(self,filename,'final_phase',None,Parameters.PrintEnable)

        filename.write("endclass : %s_agent\n"%name)
        filename.write("\n")

        # ===== Agent Callback =====
        filename.write("\t//=========================================================================\n")
        filename.write("\t// %s_agent_callback: Agent 回调基类\n"%name)
        filename.write("\t//   当需要在 agent 层面注入行为（如全局错误注入、协议拦截等）时使用\n")
        filename.write("\t//=========================================================================\n")
        filename.write("\tclass %s_agent_callback extends uvm_callback;\n"%name)
        filename.write("\t\t`uvm_object_utils(%s_agent_callback)\n"%name)
        filename.write("\t\tfunction new(string name=\"%s_agent_callback\");\n"%name)
        filename.write("\t\t\tsuper.new(name);\n")
        filename.write("\t\tendfunction\n")
        filename.write("\tendclass : %s_agent_callback\n"%name)
        filename.write("\n")

        filename.write("`endif\n")
        filename.close()

        if PrintEnable==True:
            print("[gen_uvc_agent] %s_agent.sv generated with:"%name)
            print("  - UVM_ACTIVE/UVM_PASSIVE dual mode")
            print("  - uvm_config_db-driven is_active")
            print("  - agent_callback pool for extensibility")
            print("  - rsp_port connection for driver→sequencer response")

if __name__ == '__main__':
    gen=gen_uvc_agent()
