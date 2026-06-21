/***********************************************************
 *  Copyright (C) 2026 by ChalersWang (19910619333@189.cn).
 *  All right reserved.
************************************************************/


// ============================================================================
// 模块名称: svk_rst_and_node
// 功能概述: 复位与门节点 (Reset AND Node)
//           将多个前驱复位信号 + 多个寄存器域配置位 + 多个 HDL 路径值
//           全部进行 AND 运算，得到最终期望复位值。
//           模拟 DUT 中多个复位源的硬件与门合并逻辑。
// 继承自:   svk_rst_node
// 计算公式:
//   rst = pre_nodes[0] & pre_nodes[1] & ... & pre_nodes[n]
//       & hdl_paths["a"] & hdl_paths["b"] & ...
//       & reg_fields["x"] & reg_fields["y"] & ...
// 特点:
//   - 支持任意数量的前驱节点
//   - 同时支持 hdl_path 和 reg_field 两种配置读取方式
//   - 任意输入为 0 则整体输出为 0
// ============================================================================

`ifndef SVK_RST_AND_NODE__SV
`define SVK_RST_AND_NODE__SV

class svk_rst_and_node extends svk_rst_node;
    `uvm_component_utils(svk_rst_and_node)

// ==============================================
// 构造函数: 委托 svk_rst_node::new()
// ==============================================
    function new(string name="svk_rst_and_node", uvm_component parent);
        super.new(name, parent);
    endfunction

// ==============================================
// [override] 计算 AND 复位期望值
    // rst = pre[0] & pre[1] & ... & hdl[a] & hdl[b] & ... & reg[x] & reg[y] & ...
    // 所有前驱 + 所有 hdl_paths + 所有 reg_fields 全部 AND
    // 任意输入为0 → 输出为0 (硬件多输入与门)
// ==============================================
    task get_expe_rst(output and rst);
        logic           pre_rst;
        logic           tmp;
        uvm_status_e    status;

        cfg.pre_nodes[0].get_expe_rst(rst);
        for(int i=1; i<cfg.pre_nodes.size; ++i)begin
            cfg.pre_nodes[0].get_expe_rst(pre_rst);
            rst = rst & pre_rst; 
        end

        foreach(cfg.hdl_paths[i])begin
            uvm_hdl_read(cfg.hdl_paths[i], tmp);
            rst = rst & tmp;
            `uvm_info("get_exp_rst", $sformatf("hdl_paths[%s]=%0b", i, tmp), UVM_NONE)
        end
        foreach(cfg.reg_fields[i])begin
            cfg.reg_fields[i].read(status, tmp);
            rst = rst & tmp;
            `uvm_info("get_exp_rst", $sformatf("reg_fields[%s]=%0b", i, tmp), UVM_NONE)
        end
        `uvm_info("get_expe_rst", $sformatf("%s: rst=%0b",get_name(),  rst), UVM_NONE)
    endtask

endclass


`endif
