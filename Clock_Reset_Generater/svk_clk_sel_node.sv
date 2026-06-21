/***********************************************************
 *  Copyright (C) 2026 by ChalersWang (19910619333@189.cn).
 *  All right reserved.
************************************************************/


// ============================================================================
// 模块名称: svk_clk_sel_node
// 功能概述: 时钟选择器/多路复用器节点 (Clock Selector / MUX Node)
//           根据 sel 信号选择两个前驱节点之一的时钟输出。
// 继承自:   svk_clk_node
// 关键寄存器域:
//   sel  — 选择信号 (0=选择 pre_nodes[0], 1=选择 pre_nodes[1])
// 关键方法:
//   get_expe_clk() — 根据 sel 值返回被选中前驱节点的期望时钟
//   get_pre_node() — 根据 sel 值返回被选中的前驱节点引用
// ============================================================================

`ifndef SVK_CLK_SEL_NODE__SV
`define SVK_CLK_SEL_NODE__SV

class svk_clk_sel_node extends svk_clk_node;
    `uvm_component_utils(svk_clk_sel_node)

    function new(string name="", uvm_component parent);
        super.new(name, parent);
    endfunction

    task get_expe_clk(output real period, output real duty_ratio);
        bit sel;

        if(cfg.reg_fields.exists("sel"))
            sel = cfg.reg_fields["sel"].get();
        else
            uvm_hdl_read(cfg.hdl_paths["sel"], sel);

        if(sel == 0)begin
            cfg.pre_nodes[0].get_expe_clk(period, duty_ratio);
        end
        else begin
            cfg.pre_nodes[1].get_expe_clk(period, duty_ratio);
        end

        `uvm_info("get_expe_clk", $sformatf("%s:sel=%0b, period=%0f, duty_ratio=%0f",get_name(), sel, period, duty_ratio), UVM_HIGH)
    endtask

    function svk_clk_node get_pre_node();
        int sel;

        if(cfg.reg_fields.exists("sel"))
            sel = cfg.reg_fields["sel"].get();
        else
            uvm_hdl_read(cfg.hdl_paths["sel"], sel);

        if(sel == 0)
            return cfg.pre_nodes[0];
        else
            return cfg.pre_nodes[1];

    endfunction

endclass


`endif
