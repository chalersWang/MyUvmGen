/***********************************************************
 *  Copyright (C) 2026 by ChalersWang (19910619333@189.cn).
 *  All right reserved.
************************************************************/


// ============================================================================
// 模块名称: svk_clk_gate_node
// 功能概述: 时钟门控节点 (Clock Gate Node)
//           根据 gate 信号控制时钟通断: gate=0 关闭时钟, gate=1 透传。
// 继承自:   svk_clk_node
// 关键寄存器域:
//   gate  — 门控使能 (0=关闭时钟 period=0, 1=透传前驱时钟)
// 特殊处理:
//   get_real_clk() 重写 — 当时钟关闭时沿前驱链回溯到第一个有有效时钟的节点,
//   以获取合理的前驱时钟周期来设置超时等待时间。
// ============================================================================

`ifndef SVK_CLK_GATE_NODE__SV
`define SVK_CLK_GATE_NODE__SV

class svk_clk_gate_node extends svk_clk_node;
    `uvm_component_utils(svk_clk_gate_node)

// ==============================================
// 构造函数: 委托 svk_clk_node::new()
// ==============================================
    function new(string name="", uvm_component parent);
        super.new(name, parent);
    endfunction

// ==============================================
// [override] 计算门控后期望时钟
    // gate=0 → period=0 (时钟关闭, 无时钟输出)
    // gate=1 → 透传 pre_nodes[0] 的期望时钟
// ==============================================
    task get_expe_clk(output real period, output real duty_ratio);
        bit gate;
        uvm_status_e status;

        if(cfg.reg_fields.exists("gate"))
            cfg.reg_fields["gate"].read(status, gate);
        else
            uvm_hdl_read(cfg.hdl_paths["gate"], gate);

        if(gate == 0)begin
            period     = 0;
            duty_ratio = 0;
        end
        else begin
            cfg.pre_nodes[0].get_expe_clk(period, duty_ratio);
        end

        `uvm_info("get_expe_clk", $sformatf("%s:gate=%0b, period=%0f, duty_ratio=%0f",get_name(), gate, period, duty_ratio), UVM_HIGH)
    endtask

// ==============================================
// [override] 重写实测时钟方法
    // 当时钟关闭(gate=0)时, 沿前驱链回溯找到第一个有效时钟节点
    // 以其周期设置超时等待: time_out = pre_period × 10 + 1
    // 避免因时钟关闭导致无限等待超时
// ==============================================
    task get_real_clk(output real period, output real duty_ratio, input int time_out_time=1000, input int MEAN_CYCLE_NUM=1);
        svk_clk_node  pre_node;
        real            pre_period;
        real            pre_duty_ratio;

        pre_node = get_pre_node();
        while(1)begin
            pre_node.get_expe_clk(pre_period, pre_duty_ratio);
            if(pre_period != 0)
                break;
            pre_node = pre_node.get_pre_node();    
        end

        super.get_real_clk(period, duty_ratio, pre_period * 10 + 1);

    endtask

endclass

`endif
