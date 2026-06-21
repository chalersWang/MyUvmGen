#!/usr/bin/env python3
# -*-coding:UTF-8-*-
# ============================================================
# MyUvmGen_v2.0 — UVM Register Block 代码生成器 (增强版)
#
# 【设计说明】
# - 从 Excel RegModel Sheet 读取寄存器定义
# - 自动生成完整的 UVM Register Model（RAL）
#   - 每个寄存器 → 一个 uvm_reg 派生类，含 field 定义
#   - 顶层 → xx_reg_block，含 reg_map 和 default_map
# - 替代原有的 ralf → ralgen 流程，不依赖 Synopsys VCS 工具
# - 支持多 field 寄存器（Excel 中同一 reg_name 的多行合并为同一 reg）
#
# 【UVM 方法论要点】
# - uvm_reg_field: 寄存器中的单个字段，定义位宽/访问属性/复位值
# - uvm_reg: 寄存器容器，包含多个 field
# - uvm_reg_block: 寄存器块，包含多个 reg 和 reg_map
# - uvm_reg_map: 地址映射表，定义物理地址到寄存器的映射关系
#
# 【Excel RegModel Sheet 列定义】
#   A: Register Name (多行同名 → 同寄存器多 field)
#   B: Bits (寄存器总位宽，如 32)
#   C: Field Name
#   D: Sub-Bits (field 位段，如 "7:0" 或 "8")
#   E: Access (RO/RW/WO/W1C/W1S/RC 等)
#   F: Reset Value
#   G: Description
# ============================================================
import os
import sys
import re

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from common_lib.parameters import Parameters


# UVM access 类型映射表
_ACCESS_MAP = {
    "RO": "RO", "R": "RO", "READ_ONLY": "RO",
    "WO": "WO", "W": "WO", "WRITE_ONLY": "WO",
    "RW": "RW", "R/W": "RW", "READ_WRITE": "RW",
    "W1C": "W1C", "W1S": "W1S",
    "RC": "RC", "WC": "WC", "WRC": "WRC", "WRS": "WRS",
    "RS": "RS", "WS": "WS",
}

# reg_block add_reg access 宏映射
_REG_ACCESS_MAP = {
    "RO": "RO", "R": "RO",
    "WO": "WO", "W": "WO",
    "RW": "RW", "R/W": "RW",
    "W1C": "RW", "W1S": "RW",
    "RC": "RO", "WC": "WO", "WRC": "RW", "WRS": "RW",
    "RS": "RO", "WS": "WO",
}


class gen_reg_block:

    def __init__(self):
        print("[gen_reg_block]: initial")
        self.gen_reg_block_info(tb_name='xx', PrintEnable=True)

    # ----------------------------------------------------------------
    # 辅助方法
    # ----------------------------------------------------------------
    @staticmethod
    def _na(raw):
        """规范化 access 字符串"""
        raw = str(raw).strip().upper() if raw else "RW"
        return _ACCESS_MAP.get(raw, "RW")

    @staticmethod
    def _ra(raw):
        """获取 register-level access 字符串"""
        raw = str(raw).strip().upper() if raw else "RW"
        return _REG_ACCESS_MAP.get(raw, "RW")

    @staticmethod
    def _ew(bits_str):
        """从 bits 字符串提取整数宽度"""
        try:
            return int(re.search(r'\d+', str(bits_str)).group())
        except:
            return 32

    @staticmethod
    def _ps(subbits_str):
        """解析 field 位段字符串，返回 (msb, lsb, width)"""
        s = str(subbits_str).strip()
        if not s or s.lower() == "none":
            return (0, 0, 1)
        s = s.strip("[]")
        if ':' in s:
            parts = s.split(':')
            try:
                return (int(parts[0].strip()), int(parts[1].strip()),
                        int(parts[0].strip()) - int(parts[1].strip()) + 1)
            except:
                return (0, 0, 1)
        else:
            try:
                bit = int(s)
                return (bit, bit, 1)
            except:
                return (0, 0, 1)

    @staticmethod
    def _nr(reset_raw, width):
        """规范化复位值字符串"""
        val = str(reset_raw).strip()
        if not val or val.lower() == "none":
            return "%d'h0" % width
        if val.lower().startswith("0x"):
            return "%d'h%s" % (width, val[2:])
        if "'h" in val.lower():
            return val
        try:
            return "%d'h%X" % (width, int(val))
        except:
            return "%d'h0" % width

    @staticmethod
    def _group_registers(ctx):
        """将寄存器列表按 reg_name 分组"""
        if not hasattr(ctx, 'REG_Name') or not ctx.REG_Name:
            return []

        regs = []
        seen = {}
        reg_count = len(ctx.REG_Name)
        has_subbits = hasattr(ctx, 'REG_SubBits') and ctx.REG_SubBits

        for i in range(reg_count):
            raw_name = str(ctx.REG_Name[i]).strip() if i < len(ctx.REG_Name) else "UNKNOWN"
            if not raw_name or raw_name.lower() == "none":
                continue

            if raw_name not in seen:
                bits_str = ctx.REG_Bits[i] if i < len(ctx.REG_Bits) else "32"
                width = gen_reg_block._ew(bits_str)
                raw_access = ctx.REG_Access[i] if i < len(ctx.REG_Access) else "RW"
                reg = {
                    'name': raw_name,
                    'width': width,
                    'address': len(seen) * 4,
                    'access': gen_reg_block._na(raw_access),
                    'reg_access': gen_reg_block._ra(raw_access),
                    'fields': []
                }
                seen[raw_name] = reg
                regs.append(reg)

            reg = seen[raw_name]
            field_name = str(ctx.REG_Filed[i]).strip() if i < len(ctx.REG_Filed) else "DATA"
            if not field_name or field_name.lower() == "none":
                field_name = "DATA"

            raw_access = ctx.REG_Access[i] if i < len(ctx.REG_Access) else "RW"
            access = gen_reg_block._na(raw_access)

            if has_subbits and i < len(ctx.REG_SubBits):
                msb, lsb, fwidth = gen_reg_block._ps(ctx.REG_SubBits[i])
            else:
                msb = reg['width'] - 1
                lsb = 0
                fwidth = reg['width']

            reset_raw = ctx.REG_ResetValue[i] if i < len(ctx.REG_ResetValue) else "0"
            reset = gen_reg_block._nr(reset_raw, fwidth)

            if field_name.upper() == "RESERVED":
                field_name = "RESERVED_%d" % lsb
                access = "RO"

            reg['fields'].append({
                'name': field_name.upper(), 'msb': msb, 'lsb': lsb,
                'width': fwidth, 'access': access, 'reset': reset,
            })

        return regs

    # ----------------------------------------------------------------
    # 主生成方法
    # ----------------------------------------------------------------
    def gen_reg_block_info(self, tb_name, PrintEnable=False):
        """生成完整的 UVM register block"""

        F = open("%s_reg_block.sv" % tb_name, "w+", encoding="utf-8")
        MG = "_%s_REG_BLOCK_SV_" % tb_name.upper()

        # 文件头
        F.write("`ifndef %s\n" % MG)
        F.write("`define %s\n" % MG)
        F.write("\n")
        F.write("//=========================================================================\n")
        F.write("// %s_reg_block: 自动生成的 UVM Register Block (MyUvmGen_v2.0)\n" % tb_name)
        F.write("//   包含: 每个寄存器的 uvm_reg 派生类 + 顶层 %s_reg_block\n" % tb_name)
        F.write("//=========================================================================\n")
        F.write("`include \"uvm_macros.svh\"\n")
        F.write("import uvm_pkg::*;\n")
        F.write("\n")

        regs = gen_reg_block._group_registers(self)

        if regs:
            PrintLog(self, "[gen_reg_block] 发现 %d 个寄存器" % len(regs), PrintEnable)

            # Step 1: 为每个寄存器生成 uvm_reg 类
            for reg in regs:
                F.write("//-------------------------------------------------------------------------\n")
                F.write("// 寄存器: %s\n" % reg['name'])
                F.write("//   addr=0x%02X, width=%d, access=%s\n" % (reg['address'], reg['width'], reg['access']))
                F.write("//   Fields:\n")
                for f in reg['fields']:
                    F.write("//     %s[%d:%d]  %s  reset=%s\n" % (f['name'], f['msb'], f['lsb'], f['access'], f['reset']))
                F.write("//-------------------------------------------------------------------------\n")
                F.write("class %s_reg extends uvm_reg;\n" % reg['name'])
                F.write("\n")
                for f in reg['fields']:
                    F.write("    rand uvm_reg_field %s;\n" % f['name'])
                F.write("\n")
                F.write("    `uvm_object_utils(%s_reg)\n" % reg['name'])
                F.write("\n")
                F.write("    function new(string name=\"%s_reg\");\n" % reg['name'])
                F.write("        super.new(name, %d, UVM_NO_COVERAGE);\n" % reg['width'])
                F.write("    endfunction\n")
                F.write("\n")
                F.write("    virtual function void build();\n")
                for f in reg['fields']:
                    F.write("        %s = uvm_reg_field::type_id::create(\"%s\");\n" % (f['name'], f['name']))
                    F.write("        %s.configure(this, %d, %d, \"%s\", 0, %s, 1, 1, 1);\n" % (
                        f['name'], f['width'], f['lsb'], f['access'], f['reset']))
                F.write("    endfunction\n")
                F.write("\n")
                F.write("endclass : %s_reg\n" % reg['name'])
                F.write("\n")

            # Step 2: 生成顶层 reg_block
            F.write("//=========================================================================\n")
            F.write("// %s_reg_block: 顶层寄存器块\n" % tb_name)
            F.write("//   - default_map 管理所有寄存器的地址映射\n")
            F.write("//=========================================================================\n")
            F.write("class %s_reg_block extends uvm_reg_block;\n" % tb_name)
            F.write("\n")
            for reg in regs:
                F.write("    rand %s_reg %s;\n" % (reg['name'], reg['name']))
            F.write("\n")
            F.write("    `uvm_object_utils(%s_reg_block)\n" % tb_name)
            F.write("\n")
            F.write("    function new(string name=\"%s_reg_block\");\n" % tb_name)
            F.write("        super.new(name, UVM_NO_COVERAGE);\n")
            F.write("    endfunction\n")
            F.write("\n")
            F.write("    virtual function void build();\n")
            F.write("        super.build();\n")
            F.write("        default_map = create_map(\"default_map\", 0, 4, UVM_LITTLE_ENDIAN, 0);\n")
            F.write("\n")
            for reg in regs:
                F.write("        %s = %s_reg::type_id::create(\"%s\");\n" % (reg['name'], reg['name'], reg['name']))
                F.write("        %s.configure(this, null, \"\");\n" % reg['name'])
                F.write("        %s.build();\n" % reg['name'])
                F.write("        default_map.add_reg(%s, 'h%X, \"%s\");\n" % (reg['name'], reg['address'], reg['reg_access']))
                F.write("\n")
            F.write("        lock_model();\n")
            F.write("    endfunction\n")
            F.write("\n")
            F.write("endclass : %s_reg_block\n" % tb_name)
            F.write("\n")
        else:
            F.write("// 无寄存器定义，生成空 reg_block 模板\n")
            F.write("class %s_reg_block extends uvm_reg_block;\n" % tb_name)
            F.write("\n")
            F.write("    `uvm_object_utils(%s_reg_block)\n" % tb_name)
            F.write("\n")
            F.write("    function new(string name=\"%s_reg_block\");\n" % tb_name)
            F.write("        super.new(name, UVM_NO_COVERAGE);\n")
            F.write("    endfunction\n")
            F.write("\n")
            F.write("    virtual function void build();\n")
            F.write("        super.build();\n")
            F.write("        default_map = create_map(\"default_map\", 0, 4, UVM_LITTLE_ENDIAN, 0);\n")
            F.write("        lock_model();\n")
            F.write("    endfunction\n")
            F.write("\n")
            F.write("endclass : %s_reg_block\n" % tb_name)
            F.write("\n")

        F.write("`endif // %s\n" % MG)
        F.write("\n")
        F.close()

        if PrintEnable:
            print("[gen_reg_block] %s_reg_block.sv generated" % tb_name)


def PrintLog(self, msg, enable):
    if enable:
        tag = self.tb_name if hasattr(self, 'tb_name') else "gen_reg_block"
        print("[%s] %s" % (tag, msg))


if __name__ == '__main__':
    gen = gen_reg_block()
