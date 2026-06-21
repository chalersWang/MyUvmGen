/***********************************************************
 *  Copyright (C) 2026 by ChalersWang (19910619333@189.cn).
 *  All right reserved.
************************************************************/


// ============================================================================
// 模块名称: svk_rst_wire_node
// 功能概述: 复位直通/连线节点 (Reset Wire Node)
//           最简复位节点，直接透传前驱节点的复位值，不做任何变换。
//           通常作为复位树末端节点使用 (is_end_point=1)。
// 继承自:   svk_rst_node
// 特点:
//   - get_expe_rst() 直接委托给 pre_nodes[0].get_expe_rst()
//   - 无额外配置参数
// ============================================================================

`ifndef SVK_RST_WIRE_NODE__SV
`define SVK_RST_WIRE_NODE__SV

class svk_rst_wire_node extends svk_rst_node;
    `uvm_component_utils(svk_rst_wire_node)

    function new(string name="svk_rst_wire_node", uvm_component parent);
        super.new(name, parent);
    endfunction

    task get_expe_rst(output logic rst);
        cfg.pre_nodes[0].get_expe_rst(rst);
        `uvm_info("get_expe_rst", $sformatf("%s: rst=%0b",get_name(),  rst), UVM_NONE)
    endtask

endclass


`endif
