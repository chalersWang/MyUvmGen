#! /usr/bin/env python
# -*-coding:UTF-8-*-
# ============================================================
# MyUvmGen_v2.0 — UVC Sequence 代码生成器
#
# 【设计说明】
# - 使用 `uvm_do` 宏（自动 create + randomize + send），
#   替代原先的 `uvm_send`（需要手动 create/randomize）
# - pre_body 中 raise_objection（使用 starting_phase），post_body 中 drop_objection
# - 支持从 config_db 获取 UVC 配置（%s_cfg）
# - body 中提供用户自定义区域，通过注释标记
#
# 【UVM 方法论要点】
# - uvm_do 宏 = create + start_item + randomize + finish_item，一站式
# - starting_phase 是 sequence 被启动时所在的 phase，
#   用于在 sequence 层面控制 phase objection
# - objection 必须在 pre_body raise，post_body drop，确保 body 执行期间 phase 不结束
# ============================================================
import os

from common_lib.parameters import Parameters
from common_lib.common_lib import gen_uvm_body
from common_lib.common_lib import gen_uvm_new

class gen_uvc_sequence_lib:

    def __init__(self):
        print("[gen_uvc_sequence_lib]:initial")
        self.gen_uvc_sequence_lib_info(name='xx',PrintEnable=True)

    def gen_uvc_sequence_lib_info(self,name,PrintEnable):
        filename = open("%s_sequence_lib.sv"%name, "w+")
        filename.write("`ifndef _%s_SEQUENCE_LIB_SV_\n"%name.upper())
        filename.write("`define _%s_SEQUENCE_LIB_SV_\n"%name.upper())
        filename.write("\n")

        filename.write("//=========================================================================\n")
        filename.write("// %s_base_sequence: %s UVC 的基类 sequence\n" % (name, name))
        filename.write("//   继承自 uvm_sequence，所有 %s 相关 sequence 应继承此类\n"%name)
        filename.write("//=========================================================================\n")

        # ===== Base Sequence =====
        filename.write("class %s_base_sequence extends uvm_sequence#(%s_trans);\n"%(name,name))
        filename.write("\n")
        filename.write("\t%s_config %s_cfg;\n\n"%(name,name))
        filename.write("\t`uvm_object_utils(%s_base_sequence)\n"%name)
        filename.write("\n")
        filename.write("\tfunction new(string name=\"%s_base_sequence\");\n"%name)
        filename.write("\t\tsuper.new(name);\n")
        filename.write("\tendfunction\n")
        filename.write("\n")
        
        # pre_body: raise objection + get config
        filename.write("\t// pre_body: raise objection，确保 sequence 执行期间 phase 不结束\n")
        filename.write("\tvirtual task pre_body();\n")
        filename.write("\t\t`uvm_info(get_type_name(), \"pre_body begin\", UVM_HIGH)\n")
        filename.write("\t\t// 使用 starting_phase raise objection（sequence 层面的 phase 控制）\n")
        filename.write("\t\tif (starting_phase != null)\n")
        filename.write("\t\t\tstarting_phase.raise_objection(this, get_type_name());\n")
        filename.write("\t\t// 获取 config（若不需要可注释）\n")
        filename.write("\t\tif (!uvm_config_db#(%s_config)::get(null, get_full_name(), \"%s_config\", %s_cfg))\n"%(name,name,name))
        filename.write("\t\t\t`uvm_fatal(get_type_name(), \"can not get %s_config object !!!\")\n"%name)
        filename.write("\t\t`uvm_info(get_type_name(), \"pre_body end\", UVM_HIGH)\n")
        filename.write("\tendtask : pre_body\n")
        filename.write("\n")
        
        # body: 用户自定义
        filename.write("\t// body: 用户在此实现 sequence 行为\n")
        filename.write("\t//   默认发送一笔 transaction（使用 uvm_do 宏，自动 create+randomize+send）\n")
        filename.write("\tvirtual task body();\n")
        filename.write("\t\t`uvm_info(get_type_name(), \"body begin\", UVM_MEDIUM)\n")
        filename.write("\t\t// ===== 用户代码区域 =====\n")
        filename.write("\t\t// 方式1: 使用 uvm_do 宏（推荐，一行搞定）\n")
        filename.write("\t\t// `uvm_do(req)\n")
        filename.write("\t\t//\n")
        filename.write("\t\t// 方式2: 使用 uvm_do_with 宏（带约束）\n")
        filename.write("\t\t// `uvm_do_with(req, { req.data == 8'h55; })\n")
        filename.write("\t\t//\n")
        filename.write("\t\t// 方式3: 手动控制（需要精细控制时）\n")
        filename.write("\t\t// req = %s_trans::type_id::create(\"req\");\n"%name)
        filename.write("\t\t// start_item(req);\n")
        filename.write("\t\t// assert(req.randomize());\n")
        filename.write("\t\t// finish_item(req);\n")
        filename.write("\t\t// ===== 用户代码区域结束 =====\n")
        filename.write("\t\t`uvm_info(get_type_name(), \"body end\", UVM_MEDIUM)\n")
        filename.write("\tendtask : body\n")
        filename.write("\n")

        # post_body: drop objection
        filename.write("\t// post_body: drop objection，允许 phase 正常结束\n")
        filename.write("\tvirtual task post_body();\n")
        filename.write("\t\t`uvm_info(get_type_name(), \"post_body begin\", UVM_HIGH)\n")
        filename.write("\t\tif (starting_phase != null)\n")
        filename.write("\t\t\tstarting_phase.drop_objection(this, get_type_name());\n")
        filename.write("\t\t`uvm_info(get_type_name(), \"post_body end\", UVM_HIGH)\n")
        filename.write("\tendtask : post_body\n")
        
        filename.write("endclass : %s_base_sequence\n"%name)
        filename.write("\n")

        # ===== User Sequence（空壳，待用户填充） =====
        filename.write("//=========================================================================\n")
        filename.write("// %s_demo_sequence: 示例 sequence\n"%name)
        filename.write("//   生成单笔 transaction 并发送\n")
        filename.write("//=========================================================================\n")
        filename.write("class %s_demo_sequence extends %s_base_sequence;\n"%(name,name))
        filename.write("\t`uvm_object_utils(%s_demo_sequence)\n"%name)
        filename.write("\tfunction new(string name=\"%s_demo_sequence\");\n"%name)
        filename.write("\t\tsuper.new(name);\n")
        filename.write("\tendfunction\n")
        filename.write("\tvirtual task body();\n")
        filename.write("\t\tsuper.body();  // 调用基类 body\n")
        filename.write("\t\t// 示例：发送随机 transaction\n")
        filename.write("\t\t`uvm_do(req)\n")
        filename.write("\tendtask : body\n")
        filename.write("endclass : %s_demo_sequence\n"%name)
        filename.write("\n")

        filename.write("`endif\n")
        filename.close()

        if PrintEnable==True:
            print("[gen_uvc_sequence_lib] %s_sequence_lib.sv generated with:"%name)
            print("  - uvm_do macro (auto create+randomize+send)")
            print("  - proper starting_phase objection in pre_body/post_body")
            print("  - base_sequence + demo_sequence pattern")
            print("  - user code area markers")

if __name__ == '__main__':
    gen=gen_uvc_sequence_lib()
