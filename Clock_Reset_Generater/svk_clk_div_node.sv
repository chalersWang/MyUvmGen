/***********************************************************
 *  Copyright (C) 2026 by ChalersWang (19910619333@189.cn).
 *  All right reserved.
************************************************************/


// ============================================================================
// 模块名称: svk_clk_div_node
// 功能概述: 时钟分频器节点 (Clock Divider Node)
//           从前驱节点获取时钟，根据分频系数(div)计算分频后的期望时钟。
// 继承自:   svk_clk_node
// 关键寄存器域:
//   div  — 分频系数
// 计算公式:
//   period = pre_period × (div + 1)
//   duty_ratio = 0.5 (固定50%占空比)
// ============================================================================

`ifndef SVK_CLK_DIV_NODE__SV
`define SVK_CLK_DIV_NODE__SV

class svk_clk_div_node extends svk_clk_node;
    `uvm_component_utils(svk_clk_div_node)

    function new(string name="", uvm_component parent);
        super.new(name, parent);
    endfunction

    task get_expe_clk(output real period, output real duty_ratio);
        real pre_duty_ratio;
        real pre_period;

        int div;

        if(cfg.reg_fields.exists("div"))
            div = cfg.reg_fields["div"].get();
        else
            uvm_hdl_read(cfg.hdl_paths["div"], div);

        cfg.pre_nodes[0].get_expe_clk(pre_period, pre_duty_ratio);

        period     = pre_period * (div + 1);






        duty_ratio = 0.5;
        if(period == 0)
            duty_ratio = 0;

        `uvm_info("get_expe_clk", $sformatf("%s:div=%0d period=%0f, duty_ratio=%0f",get_name(), div, period, duty_ratio), UVM_HIGH)
    endtask

endclass


`endif