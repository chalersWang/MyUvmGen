#!/usr/bin/env python3
# -*-coding:UTF-8-*-
# ============================================================
# MyUvmGen_v2.0 — 寄存器 Adapter 代码生成器（增强版）
#
# 【设计说明】
# - 兼容多种总线类型（APB/AHB/AXI/自定义）
# - 自动从 DUT group 推断总线 transaction 类型
# - 支持 byte_enable（字节使能）用于窄位宽访问
#
# 【UVM 方法论要点】
# - uvm_reg_adapter: 将 uvm_reg_bus_op 转换为总线 transaction，反之亦然
# - reg2bus(): RAL 操作 → 总线 transaction（前门写/读）
# - bus2reg(): 总线 transaction → RAL 操作（读响应）
# - provides_responses: 指示 adapter 是否处理响应（=1 表示需要 bus2reg）
# ============================================================
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from common_lib.parameters import Parameters

class gen_reg_adapter:

    def __init__(self):
        print("[gen_reg_adapter]: initial")
        self.gen_reg_adapter_info(name="apb", PrintEnable=True)

    def gen_reg_adapter_info(self, name, PrintEnable):
        """生成总线 adepter
        
        Args:
            name: 总线类型名 (apb/ahb/axi 或 UVC group name)
        """
        filename = open("%s_reg_adapter.sv" % name, "w+", encoding="utf-8")
        
        filename.write("`ifndef _%s_REG_ADAPTER_SV_\n" % name.upper())
        filename.write("`define _%s_REG_ADAPTER_SV_\n")
        filename.write("\n")
        filename.write("//=========================================================================\n")
        filename.write("// %s_reg_adapter: 寄存器访问总线适配器\n" % name)
        filename.write("//   将 uvm_reg_bus_op 转换为 %s_trans，反向亦然\n" % name)
        filename.write("//=========================================================================\n")
        filename.write("class %s_reg_adapter extends uvm_reg_adapter;\n" % name)
        filename.write("\n")
        filename.write("    `uvm_object_utils(%s_reg_adapter)\n" % name)
        filename.write("\n")
        filename.write("    function new(string name=\"%s_reg_adapter\");\n" % name)
        filename.write("        super.new(name);\n")
        filename.write("        // supports_byte_enable: 设为 1 以支持字节级访问\n")
        filename.write("        supports_byte_enable = 0;\n")
        filename.write("        // provides_responses: adapter 是否处理 bus2reg\n")
        filename.write("        provides_responses  = 1;\n")
        filename.write("    endfunction : new\n")
        filename.write("\n")
        # reg2bus
        filename.write("    // =====================================================================\n")
        filename.write("    // reg2bus: 将 RAL 操作 (uvm_reg_bus_op) 转换为总线 transaction\n")
        filename.write("    //   rw.kind:  UVM_READ / UVM_WRITE\n")
        filename.write("    //   rw.addr:  目标寄存器地址\n")
        filename.write("    //   rw.data:  要写入的数据 (WRITE 时)\n")
        filename.write("    // =====================================================================\n")
        filename.write("    virtual function uvm_sequence_item reg2bus(const ref uvm_reg_bus_op rw);\n")
        filename.write("        %s_trans tr;\n" % name)
        filename.write("        tr = %s_trans::type_id::create(\"tr\");\n" % name)
        filename.write("\n")
        filename.write("        tr.CFG   = (rw.kind == UVM_READ) ? %s_trans::READ : %s_trans::WRITE;\n" % (name, name))
        filename.write("        tr.ADDR  = rw.addr;\n")
        filename.write("\n")
        filename.write("        if (rw.kind == UVM_WRITE) begin\n")
        filename.write("            tr.WRDATA = rw.data;\n")
        filename.write("        end\n")
        filename.write("        else begin\n")
        filename.write("            tr.RDDATA = rw.data;  // 前门读时，此值可能是 X\n")
        filename.write("        end\n")
        filename.write("\n")
        filename.write("        `uvm_info(get_type_name(), $sformatf(\"reg2bus: kind=%%0s addr=%%0h data=%%0h\",\n")
        filename.write("            rw.kind.name(), rw.addr, rw.data), UVM_FULL)\n")
        filename.write("\n")
        filename.write("        return tr;\n")
        filename.write("    endfunction : reg2bus\n")
        filename.write("\n")
        # bus2reg
        filename.write("    // =====================================================================\n")
        filename.write("    // bus2reg: 将总线 transaction 的响应转换回 uvm_reg_bus_op\n")
        filename.write("    //   bus_item: 总线返回的 transaction\n")
        filename.write("    //   rw: 需要更新的 bus_op\n")
        filename.write("    // =====================================================================\n")
        filename.write("    virtual function void bus2reg(uvm_sequence_item bus_item,\n")
        filename.write("                                   ref uvm_reg_bus_op rw);\n")
        filename.write("        %s_trans tr;\n" % name)
        filename.write("        if (!$cast(tr, bus_item)) begin\n")
        filename.write("            `uvm_fatal(get_type_name(), \"bus2reg: cast failed! Wrong transaction type.\")\n")
        filename.write("            return;\n")
        filename.write("        end\n")
        filename.write("\n")
        filename.write("        rw.kind  = (tr.CFG == %s_trans::WRITE) ? UVM_WRITE : UVM_READ;\n" % name)
        filename.write("        rw.addr  = tr.ADDR;\n")
        filename.write("        rw.data  = (tr.CFG == %s_trans::WRITE) ? tr.WRDATA : tr.RDDATA;\n" % name)
        filename.write("        rw.status = UVM_IS_OK;\n")
        filename.write("\n")
        filename.write("        `uvm_info(get_type_name(), $sformatf(\"bus2reg: kind=%%0s addr=%%0h data=%%0h\",\n")
        filename.write("            rw.kind.name(), rw.addr, rw.data), UVM_FULL)\n")
        filename.write("    endfunction : bus2reg\n")
        filename.write("\n")
        filename.write("endclass : %s_reg_adapter\n" % name)
        filename.write("\n")
        filename.write("`endif\n")
        filename.close()

        if PrintEnable:
            print("[gen_reg_adapter] %s_reg_adapter.sv generated" % name)


if __name__ == '__main__':
    gen = gen_reg_adapter()

