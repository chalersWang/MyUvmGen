/***********************************************************
 *  Copyright (C) 2026 by ChalersWang (19910619333@189.cn).
 *  All right reserved.
************************************************************/


// ============================================================================
// 模块名称: svk_rst_sync_node
// 功能概述: 同步复位节点 (Synchronous Reset Node)
//           直接透传前驱节点的复位值，通常在 cfg 中配置 sync_check_en=1
//           以自动检测复位释放是否与时钟同步。
// 继承自:   svk_rst_node
// 特点:
//   - get_expe_rst() 直接委托给 pre_nodes[0].get_expe_rst()
//   - 配合 cfg.ci (时钟接口) 和 cfg.sync_check_en 进行同步校验
// ============================================================================

`ifndef SVK_RST_SYNC_NODE__SV
`define SVK_RST_SYNC_NODE__SV

class svk_rst_sync_node extends svk_rst_node;
    `uvm_component_utils(svk_rst_sync_node)

    function new(string name="svk_rst_sync_node", uvm_component parent);
        super.new(name, parent);
    endfunction

    task get_expe_rst(output logic rst);
        cfg.pre_nodes[0].get_expe_rst(rst);
        `uvm_info("get_expe_rst", $sformatf("%s: rst=%0b",get_name(),  rst), UVM_NONE)
    endtask

endclass


`endif
