#! /usr/bin/env python
# -*-coding:UTF-8-*-
# ============================================================
# MyUvmGen_v2.0 — Transaction 代码生成器
#
# 【设计说明】
# - 根据 Excel 配置的 DUT 信号列表，自动生成 rand 成员变量
# - 使用 uvm_field_int/uvm_field_sarray_int 注册字段
# - 内建 do_copy/do_compare/do_print 可选择性 override
# - 添加详细的中文 field 机制说明注释
#
# 【UVM 方法论要点】
# - uvm_field_* 宏是 UVM 自动化的核心，驱动 copy/compare/print/pack/unpack
# - 位宽 > 1 的信号应使用 uvm_field_int，配合位宽参数
# - 数组信号应使用 uvm_field_sarray_int（定宽数组）或 uvm_field_array_int（动态数组）
# ============================================================
import os
import re
from common_lib.parameters import Parameters

class gen_uvc_trans:

    def __init__(self):
        print("[gen_uvc_trans]:initial")
        uvc_name='aa'
        uvc_signals=    "            \
                        input a     ,\
                        input[1:0]b ,\
                        output c    ,\
                        output[2:0]d,\
                        "
        self.gen_uvc_trans_info(uvc_name,uvc_signals,PrintEnable=True)

    def gen_uvc_trans_info(self,name,SIGNALS,PrintEnable):
        # 解析 SIGNALS 字符串
        Signals0=SIGNALS.replace('\n','')
        Signals1=Signals0.replace('input','')
        Signals2=Signals1.replace('output','')
        Signals2=Signals2.replace('inout','')
        Signals3=Signals2.replace(' ','')
        Signals4=Signals3.rstrip(',')
        Signals5=Signals4.split(',')
        
        # 提取信号名和位宽
        parsed_signals = []
        for sig in Signals5:
            width = 0
            sname = sig
            m = re.search(r'\[(\d+):(\d+)\]', sig)
            if m:
                hi, lo = int(m.group(1)), int(m.group(2))
                width = abs(hi - lo) + 1
                sname = re.sub(r'\[.*?\]', '', sig)
            elif re.search(r'\[(\d+)\]', sig):
                m2 = re.search(r'\[(\d+)\]', sig)
                width = int(m2.group(1))
                sname = re.sub(r'\[.*?\]', '', sig)
            parsed_signals.append({'name': sname, 'width': width})

        filename = open("%s_trans.sv"%name, "w+", encoding="utf-8")
        filename.write("`ifndef _%s_TRANS_SV_\n"%name.upper())
        filename.write("`define _%s_TRANS_SV_\n")
        filename.write("\n")
        
        # ===== UVM Field 机制详解注释 =====
        filename.write("//=========================================================================\n")
        filename.write("// %s_trans: %s UVC 的 Transaction 类\n" % (name, name))
        filename.write("//\n")
        filename.write("// 【UVM Field 机制说明】\n")
        filename.write("// uvm_field 宏驱动 UVM 自动化操作，通过 FLAG 控制行为：\n")
        filename.write("//\n")
        filename.write("// 基础宏：\n")
        filename.write("//   `uvm_field_int(ARG, FLAG)           — 整型变量\n")
        filename.write("//   `uvm_field_enum(T, ARG, FLAG)       — 枚举变量\n")
        filename.write("//   `uvm_field_object(ARG, FLAG)        — 对象引用\n")
        filename.write("//   `uvm_field_string(ARG, FLAG)        — 字符串\n")
        filename.write("//   `uvm_field_event(ARG, FLAG)         — 事件\n")
        filename.write("//\n")
        filename.write("// 数组宏：\n")
        filename.write("//   `uvm_field_sarray_int(ARG, FLAG)    — 定宽整型数组\n")
        filename.write("//   `uvm_field_array_int(ARG, FLAG)     — 动态整型数组\n")
        filename.write("//   `uvm_field_queue_int(ARG, FLAG)     — 队列\n")
        filename.write("//\n")
        filename.write("// FLAG 控制位（可组合）：\n")
        filename.write("//   UVM_ALL_ON     = 开启所有操作（copy/compare/print/record/pack）\n")
        filename.write("//   UVM_DEFAULT    = 除 radix 外的所有操作\n")
        filename.write("//   UVM_NOPACK     = 关闭 pack（节省内存，推荐大多数场景）\n")
        filename.write("//   UVM_NOCOMPARE  = 关闭 compare\n")
        filename.write("//   UVM_NOPRINT    = 关闭 print\n")
        filename.write("//\n")
        filename.write("// 【推荐配置】\n")
        filename.write("//   - 大型 transaction（>100 字段）：使用 UVM_NOPACK 节省内存\n")
        filename.write("//   - 调试阶段：使用 UVM_ALL_ON 方便查看\n")
        filename.write("//   - 回归测试：使用 UVM_DEFAULT | UVM_NOPACK 提速\n")
        filename.write("//=========================================================================\n")
        filename.write("class %s_trans extends uvm_sequence_item;\n"%name)
        filename.write("\n")
        
        # rand 变量声明
        filename.write("\t// ===== 随机化变量（对应 DUT 接口信号） =====\n")
        for sig in parsed_signals:
            if sig['width'] > 1:
                filename.write("\trand logic [%d:0] %-20s // [%d:0]\n"%(sig['width']-1, sig['name']+';', sig['width']-1))
            else:
                filename.write("\trand logic         %-20s // 1-bit\n"%(sig['name']+';'))
        filename.write("\n")
        filename.write("\t// ===== 约束（用户可通过 override 扩展） =====\n")
        filename.write("\t// constraint c_default {\n")
        filename.write("\t//     // 用户在此添加默认约束\n")
        filename.write("\t//     // soft data inside {[0:255]};  // 软约束示例\n")
        filename.write("\t// }\n")
        filename.write("\n")
        
        # utils_begin 注册
        filename.write("\t`uvm_object_utils_begin(%s_trans)\n"%name)
        for sig in parsed_signals:
            if sig['width'] > 1:
                # 多比特用 uvm_field_int 配合位宽参数
                filename.write("\t\t`uvm_field_int(%s, UVM_ALL_ON)\n"%sig['name'])
            else:
                filename.write("\t\t`uvm_field_int(%s, UVM_ALL_ON)\n"%sig['name'])
        filename.write("\t`uvm_object_utils_end\n")
        filename.write("\n")
        
        # new()
        filename.write("\tfunction new(string name=\"%s_trans\");\n"%name)
        filename.write("\t\tsuper.new(name);\n")
        filename.write("\tendfunction : new\n")
        filename.write("\n")
        
        # do_copy/do_compare/do_print（可选 override）
        filename.write("\t// ===== 以下方法可选择性 override 以实现自定义行为 =====\n")
        filename.write("\t// 如果不 override，则使用 uvm_field 宏的默认实现\n")
        filename.write("\t// 注意：如果 override 了 do_*，需要同时修改 uvm_field 注册内容\n")
        filename.write("\n")
        filename.write("\t// 自定义 copy（如不需要，保持注释即可使用 field 自动化）\n")
        filename.write("\t// function void do_copy(uvm_object rhs);\n")
        filename.write("\t//     %s_trans rhs_;\n"%name)
        filename.write("\t//     if(!$cast(rhs_, rhs)) begin\n")
        filename.write("\t//         `uvm_fatal(\"do_copy\", \"cast failed\")\n")
        filename.write("\t//         return;\n")
        filename.write("\t//     end\n")
        filename.write("\t//     super.do_copy(rhs);\n")
        for sig in parsed_signals:
            filename.write("\t//     this.%s = rhs_.%s;\n"%(sig['name'], sig['name']))
        filename.write("\t// endfunction\n")
        filename.write("\n")
        filename.write("\t// 自定义 compare\n")
        filename.write("\t// function bit do_compare(uvm_object rhs, uvm_comparer comparer);\n")
        filename.write("\t//     %s_trans rhs_;\n"%name)
        filename.write("\t//     if(!$cast(rhs_, rhs)) return 0;\n")
        filename.write("\t//     return (super.do_compare(rhs, comparer) &&\n")
        for i, sig in enumerate(parsed_signals):
            if i == 0:
                filename.write("\t//             this.%s === rhs_.%s"%(sig['name'], sig['name']))
            else:
                filename.write(" &&\n\t//             this.%s === rhs_.%s"%(sig['name'], sig['name']))
        filename.write(");\n")
        filename.write("\t// endfunction\n")
        filename.write("\n")
        filename.write("\t// 自定义 convert2string（用于 print/sprintf）\n")
        filename.write("\t// function string convert2string();\n")
        filename.write("\t//     return $sformatf(\"%s\", super.convert2string());\n")
        filename.write("\t// endfunction\n")
        filename.write("\n")
        
        filename.write("endclass : %s_trans\n"%name)
        filename.write("\n")
        filename.write("`endif\n")
        filename.close()

        if PrintEnable==True:
            print("[gen_uvc_trans] %s_trans.sv generated with:"%name)
            print("  - auto-detected signal bit widths")
            print("  - uvm_field_int for per-signal registration")
            print("  - do_copy/do_compare/do_print template (commented)")
            print("  - constraint placeholder")
            print("  - comprehensive field mechanism documentation")

if __name__ == '__main__':
    gen=gen_uvc_trans()
