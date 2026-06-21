/***********************************************************
 *  Copyright (C) 2026 by ChalersWang (19910619333@189.cn).
 *  All right reserved.
************************************************************/


// ============================================================================
// 模块名称: svk_crg_pkg
// 功能概述: Clock & Reset Generator 顶层 Package
//           聚合所有时钟和复位节点类的包，在 package 作用域内 `include 所有
//           class 定义文件和 interface 文件，是 CRG 验证组件库的入口。
// 包含内容:
//   接口层:  svk_clk_if, svk_rst_if
//   配置层:  svk_clk_node_cfg, svk_rst_node_cfg
//   基类层:  svk_clk_node, svk_rst_node
//   时钟节点: drv_node, pll_node, div_node, sel_node, gate_node, wire_node
//   复位节点: drv_node, cfg_node, and_node, sel_node, sync_node, wire_node
//   编排层:  svk_crg, crg_nodes
// 依赖:      uvm_pkg (UVM 1.2)
// ============================================================================

`ifndef SVK_CRG_PKG__SV
`define SVK_CRG_PKG__SV

`include "svk_clk_if.sv"
`include "svk_rst_if.sv"

package svk_crg_pkg;

    import uvm_pkg::*;

    `include "svk_clk_node_cfg.sv"
    `include "svk_clk_node.sv"
    `include "svk_clk_pll_node.sv"
    `include "svk_clk_div_node.sv"
    `include "svk_clk_sel_node.sv"
    `include "svk_clk_gate_node.sv"
    `include "svk_clk_drv_node.sv"
    `include "svk_clk_wire_node.sv"

    `include "svk_rst_node_cfg.sv"
    `include "svk_rst_node.sv"
    `include "svk_rst_drv_node.sv"
    `include "svk_rst_cfg_node.sv"
    `include "svk_rst_logic_node.sv"
    `include "svk_rst_sync_node.sv"
    `include "svk_rst_wire_node.sv"

    `include "svk_crg.sv"
    `include "crg_nodes.sv"
endpackage

`endif
