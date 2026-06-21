/***********************************************************
 *  Copyright (C) 2026 by ChalersWang (19910619333@189.cn).
 *  All right reserved.
************************************************************/


// ============================================================================
// 模块名称: svk_rst_drv_node
// 功能概述: 复位驱动源节点 (Reset Driver Node)
//           复位树的根节点/叶子节点，直接驱动物理复位线。
//           期望复位值 = svk_rst_if 的当前实际值 (ri.rst)。
// 继承自:   svk_rst_node
// 特点:
//   - get_expe_rst() 直接返回 ri.rst
//   - 通常 is_active=1 以产生实际复位序列
// ============================================================================

`ifndef SVK_RST_DRV_NODE__SV
`define SVK_RST_DRV_NODE__SV

class svk_rst_drv_node extends svk_rst_node;
    `uvm_component_utils(svk_rst_drv_node)

// ==============================================
// 构造函数: 委托 svk_rst_node::new()
// ==============================================
    function new(string name="svk_rst_drv_node", uvm_component parent);
        super.new(name, parent);
    endfunction

// ==============================================
// [override] 计算驱动源期望复位值
    // 直接返回物理接口 ri.rst 的当前值 (驱动源是根节点)
// ==============================================
    task get_expe_rst(output logic rst);
        rst = cfg.ri.rst;
        `uvm_info("get_expe_rst", $sformatf("%s: rst=%0b",get_name(),  rst), UVM_NONE)
    endtask

endclass


`endif
