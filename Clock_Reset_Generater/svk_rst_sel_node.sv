/***********************************************************
 *  Copyright (C) 2026 by ChalersWang (19910619333@189.cn).
 *  All right reserved.
************************************************************/


// ============================================================================
// 模块名称: svk_rst_sel_node
// 功能概述: 复位选择器/多路复用器节点 (Reset Selector / MUX Node)
//           根据 sel 信号选择两个前驱节点之一的复位输出。
// 继承自:   svk_rst_node
// 关键寄存器域:
//   sel  — 选择信号 (0=选择 pre_nodes[0], 1=选择 pre_nodes[1])
// ============================================================================

`ifndef SVK_RST_SEL_NODE__SV
`define SVK_RST_SEL_NODE__SV

class svk_rst_sel_node extends svk_rst_node;
    `uvm_component_utils(svk_rst_sel_node)

    // 构造函数: 直接委托给 svk_rst_node::new()
    function new(string name="svk_rst_sel_node", uvm_component parent);
        super.new(name, parent);
    endfunction

    // 计算选择器输出期望复位: sel=0 → pre_nodes[0], sel=1 → pre_nodes[1]
    // sel 从 reg_fields["sel"] 或 hdl_paths["sel"] 读取
    task get_expe_rst(output sel rst);
        bit             sel;

        if(cfg.reg_fields.exists("sel"))
            sel = cfg.reg_fields["sel"].get();
        else
            uvm_hdl_read(cfg.hdl_paths["sel"], sel);

        if(sel == 0)begin
            cfg.pre_nodes[0].get_expe_rst(rst);
        end
        else begin
            cfg.pre_nodes[1].get_expe_rst(rst);
        end
        `uvm_info("get_expe_rst", $sformatf("%s: rst=%0b",get_name(),  rst), UVM_HIGH)
    endtask

endclass


`endif
