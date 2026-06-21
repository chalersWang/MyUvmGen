#! /usr/bin/env python
# -*-coding:UTF-8-*-
# ============================================================
# MyUvmGen_v2.0 — Config/Event 对象代码生成器
#
# 【设计说明】
# - %s_config: 验证环境全局配置（统一管理所有 UVC/VIP 配置）
# - 使用 uvm_config_db 发布到组件层次结构（非 null scope）
# - 包含 drain_time、verbosity 等全局控制参数
# - %s_event: 已被 uvm_event_pool 替代，保留仅为向后兼容
#
# 【UVM 方法论要点】
# - config_db 的 scope 应为具体组件路径（如 "*.env.*"），
#   而非 null（全局），避免多实例配置覆盖
# - 大型项目中建议将 config 对象直接通过 builder 传递（set + get），
#   而非全部依赖 config_db（config_db 本质是全局注册表）
# - uvm_event_pool 更适合跨组件同步（如时钟就绪、复位完成信号）
# ============================================================
import os
from common_lib.parameters import Parameters
from common_lib.common_lib import gen_uvm_new
from common_lib.common_lib import gen_uvm_phase

class gen_common_config:

    def __init__(self):
        print("[gen_common_config]:initial")
        self.gen_common_config_info(name='xx',PrintEnable=True)

    def gen_common_config_info(self,name,PrintEnable):
        filename = open("%s_config.sv"%name, "w+")
        filename.write("`ifndef _%s_CONFIG_SV_\n"%name.upper())
        filename.write("`define _%s_CONFIG_SV_\n"%name.upper())
        filename.write("\n")

        filename.write("//=========================================================================\n")
        filename.write("// %s_config: 全局验证环境配置类\n"%name)
        filename.write("//   集中管理所有子组件的配置参数\n")
        filename.write("//   通过 uvm_config_db#(%s_config)::set/get 在层次间传递\n"%name)
        filename.write("//=========================================================================\n")
        filename.write("class %s_config extends uvm_object;\n"%name)
        filename.write("\n")

        # 全局控制参数
        filename.write("\t// ===== 全局仿真控制参数 =====\n")
        filename.write("\tint        drain_time       = 100;  // main_phase 结束前的 drain 时钟数\n")
        filename.write("\tint        max_quit_count   = 0;    // 最大允许 UVM_ERROR 数（0=不限）\n")
        filename.write("\tint        verbosity        = UVM_MEDIUM;  // 全局日志级别\n")
        filename.write("\tbit        coverage_enable  = 1;    // 是否启用覆盖率收集\n")
        filename.write("\tbit        check_enable     = 1;    // 是否启用 scoreboard 比对\n")
        filename.write("\tbit        xz_check_enable  = 1;    // 是否启用 X/Z 检查\n")
        filename.write("\n")

        filename.write("\t// ===== UVM Event Pool（跨组件同步，替代独立 event 类） =====\n")
        filename.write("\t// 使用方式: uvm_event_pool::get_global(\"clk_ready\").trigger();\n")
        filename.write("\t// 不再使用独立的 xx_event 类，减少对象传递开销\n")
        filename.write("\n")

        filename.write("\t`uvm_object_utils_begin(%s_config)\n"%name)
        filename.write("\t\t`uvm_field_int(drain_time,       UVM_ALL_ON)\n")
        filename.write("\t\t`uvm_field_int(max_quit_count,   UVM_ALL_ON)\n")
        filename.write("\t\t`uvm_field_int(verbosity,        UVM_ALL_ON)\n")
        filename.write("\t\t`uvm_field_int(coverage_enable,  UVM_ALL_ON)\n")
        filename.write("\t\t`uvm_field_int(check_enable,     UVM_ALL_ON)\n")
        filename.write("\t\t`uvm_field_int(xz_check_enable,  UVM_ALL_ON)\n")
        filename.write("\t`uvm_object_utils_end\n")
        filename.write("\n")

        filename.write("\tfunction new(string name=\"%s_config\");\n"%name)
        filename.write("\t\tsuper.new(name);\n")
        filename.write("\tendfunction : new\n")
        filename.write("\n")

        filename.write("endclass : %s_config\n"%name)
        filename.write("\n")
        filename.write("`endif\n")
        filename.close()

        if PrintEnable==True:
            print("[gen_common_config] %s_config.sv generated with:"%name)
            print("  - drain_time, verbosity, max_quit_count params")
            print("  - coverage/check/xz_check enable flags")
            print("  - uvm_event_pool strategy (replacing standalone event class)")

class gen_common_event:

    def __init__(self):
        print("[gen_common_event]:initial")
        self.gen_common_event_info(name='xx',PrintEnable=True)

    def gen_common_event_info(self,name,PrintEnable):
        # ===== 生成 event.sv（保留向后兼容，但标记为 deprecated） =====
        filename = open("%s_event.sv"%name, "w+")
        filename.write("`ifndef _%s_EVENT_SV_\n"%name.upper())
        filename.write("`define _%s_EVENT_SV_\n"%name.upper())
        filename.write("\n")
        filename.write("//=========================================================================\n")
        filename.write("// %s_event: 【已废弃】保留仅为向后兼容\n"%name)
        filename.write("//   新设计应使用 uvm_event_pool::get_global() 直接获取全局事件\n")
        filename.write("//   例如: uvm_event_pool::get_global(\"clk_evt\").trigger();\n")
        filename.write("//=========================================================================\n")
        filename.write("class %s_event extends uvm_object;\n"%name)
        filename.write("\n")
        filename.write("\t`uvm_object_utils(%s_event)\n"%name)
        filename.write("\n")
        filename.write("\tfunction new(string name=\"%s_event\");\n"%name)
        filename.write("\t\tsuper.new(name);\n")
        filename.write("\tendfunction : new\n")
        filename.write("\n")
        filename.write("endclass : %s_event\n"%name)
        filename.write("\n")
        filename.write("`endif\n")
        filename.close()

        if PrintEnable==True:
            print("[gen_common_event] %s_event.sv generated (deprecated, use uvm_event_pool)"%name)

if __name__ == '__main__':
    gen_cfg = gen_common_config()
    gen_evt = gen_common_event()
