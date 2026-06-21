/***********************************************************
 *  Copyright (C) 2026 by ChalersWang (19910619333@189.cn).
 *  All right reserved.
************************************************************/


// ============================================================================
// 模块名称: svk_clk_wire_node
// 功能概述: 时钟直通/连线节点 (Clock Wire Node)
//           最简时钟节点，直接透传前驱节点的时钟参数，不做任何变换。
//           通常作为时钟树末端节点使用 (is_end_point=1)。
// 继承自:   svk_clk_node
// 特点:
//   - get_expe_clk() 直接委托给 pre_nodes[0].get_expe_clk()
//   - 无额外配置参数
// ============================================================================

`ifndef SVK_CLK_WIRE_NODE__SV
`define SVK_CLK_WIRE_NODE__SV

class svk_clk_wire_node extends svk_clk_node;
    `uvm_component_utils(svk_clk_wire_node)

// ==============================================
// 构造函数: 委托 svk_clk_node::new()
// ==============================================
    function new(string name="", uvm_component parent);
        super.new(name, parent);
    endfunction

// ==============================================
// [override] 透传前驱时钟
    // 直接委托给 pre_nodes[0].get_expe_clk(), 不做任何变换
    // 通常作为时钟树末端节点 (is_end_point=1)
// ==============================================
    task get_expe_clk(output real period, output real duty_ratio);
        cfg.pre_nodes[0].get_expe_clk(period, duty_ratio);
        `uvm_info("get_expe_clk", $sformatf("%s:period=%0f, duty_ratio=%0f",get_name(),  period, duty_ratio), UVM_HIGH)
    endtask

endclass

`endif