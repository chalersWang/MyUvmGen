/***********************************************************
 *  Copyright (C) 2026 by ChalersWang (19910619333@189.cn).
 *  All right reserved.
************************************************************/


// ============================================================================
// 模块名称: svk_clk_drv_node
// 功能概述: 时钟驱动源节点 (Clock Driver Node)
//           时钟树的根节点/叶子节点，直接驱动物理时钟线。
//           期望时钟 = 其 svk_clk_if 的 period / duty_ratio 配置值。
// 继承自:   svk_clk_node
// 特点:
//   - 没有前驱节点 (get_pre_node() 调用会报 UVM_ERROR)
//   - get_expe_clk() 直接返回 ci.period / ci.duty_ratio
//   - 通常 is_active=1 以产生实际时钟
// ============================================================================

`ifndef SVK_CLK_DRV_NODE__SV
`define SVK_CLK_DRV_NODE__SV

class svk_clk_drv_node extends svk_clk_node;
    `uvm_component_utils(svk_clk_drv_node)

// ==============================================
// 构造函数: 委托 svk_clk_node::new()
// ==============================================
    function new(string name="", uvm_component parent);
        super.new(name, parent);
    endfunction

// ==============================================
// [override] 计算驱动源期望时钟
    // 驱动源是时钟树根节点, 直接返回 ci.period / ci.duty_ratio
    // 无需递归 (无前驱节点)
// ==============================================
    task get_expe_clk(output real period, output real duty_ratio);
        period      = cfg.ci.period;
        duty_ratio  = cfg.ci.duty_ratio;
        `uvm_info("get_expe_clk", $sformatf("%s:period=%0f, duty_ratio=%0f",get_name(), period, duty_ratio), UVM_HIGH)
    endtask

// ==============================================
// [override] 驱动源无前驱节点
    // 调用此方法 → UVM_ERROR (根节点禁止获取前驱)
// ==============================================
    function svk_clk_node get_pre_node();
        `uvm_error("get_pre_node", "should not call this function")
        return null;
    endfunction

endclass



`endif