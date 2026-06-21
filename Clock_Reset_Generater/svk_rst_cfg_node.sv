/***********************************************************
 *  Copyright (C) 2026 by ChalersWang (19910619333@189.cn).
 *  All right reserved.
************************************************************/


// ============================================================================
// 模块名称: svk_rst_cfg_node
// 功能概述: 可配置复位节点 (Configurable Reset Node)
//           将前驱节点复位值与一个配置位进行 AND 操作。
//           模拟 DUT 中可通过寄存器控制的复位门控。
// 继承自:   svk_rst_node
// 关键寄存器域:
//   cfg  — 配置位
// 计算公式:
//   rst = pre_rst & cfg_bit
//   若 cfg_bit=0 → 复位被屏蔽 (始终释放), cfg_bit=1 → 透传 pre_rst
// ============================================================================

`ifndef SVK_RST_CFG_NODE__SV
`define SVK_RST_CFG_NODE__SV

class svk_rst_cfg_node extends svk_rst_node;
    `uvm_component_utils(svk_rst_cfg_node)

    // 构造函数: 直接委托给 svk_rst_node::new()
    function new(string name="svk_rst_cfg_node", uvm_component parent);
        super.new(name, parent);
    endfunction

    // 计算可配置复位期望值: rst = pre_rst & cfg_bit
    // cfg_bit 从 reg_fields["cfg"] 或 hdl_paths["cfg"] 读取
    // cfg_bit=0 → 复位被屏蔽 (始终高), cfg_bit=1 → 透传 pre_rst
    task get_expe_rst(output logic rst);
        logic           pre_rst;
        bit             cfg_rst;
        uvm_status_e    status;

        if(cfg.reg_fields.exists("cfg"))begin
            cfg.reg_fields["cfg"].read(status, cfg_rst);
        end
        else begin
            uvm_hdl_read(cfg.hdl_paths["cfg"], cfg_rst);
        end
        
        cfg.pre_nodes[0].get_expe_rst(pre_rst);

        rst = pre_rst & cfg_rst;

        `uvm_info("get_expe_rst", $sformatf("%s: cfg_rst=%0b, rst=%0b",get_name(),  cfg_rst, rst), UVM_NONE)
    endtask

endclass


`endif
