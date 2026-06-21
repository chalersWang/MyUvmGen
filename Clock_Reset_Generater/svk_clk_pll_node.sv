/***********************************************************
 *  Copyright (C) 2026 by ChalersWang (19910619333@189.cn).
 *  All right reserved.
************************************************************/


// ============================================================================
// 模块名称: svk_clk_pll_node
// 功能概述: PLL 锁相环时钟节点 (PLL Node)
//           模拟 PLL 行为，从寄存器模型读取 PLL 分频系数，递归获取前驱节点
//           时钟参数，计算出 PLL 输出时钟的期望周期和占空比。
// 继承自:   svk_clk_node
// 关键寄存器域 (reg_fields[] 或 hdl_paths[]):
//   lock     — PLL 锁定标志 (1=已锁定才能计算)
//   dsmen    — DSM (Delta-Sigma Modulator) 使能
//   refdiv   — 参考时钟分频系数
//   fbdiv    — 反馈分频系数 (整数部分)
//   frac     — 反馈分频系数 (小数部分, 24位精度)
//   postdiv1 — 后分频器1
//   postdiv2 — 后分频器2
// 计算公式:
//   DSM关闭: period = pre_period × refdiv / fbdiv
//   DSM使能: period = pre_period × refdiv / (fbdiv + frac / 2^24)
//   若 PLL 未 lock → UVM_ERROR
// ============================================================================

`ifndef SVK_CLK_PLL_NODE__SV
`define SVK_CLK_PLL_NODE__SV

class svk_clk_pll_node extends svk_clk_node;
    `uvm_component_utils(svk_clk_pll_node)

// ==============================================
// 构造函数: 委托 svk_clk_node::new()
// ==============================================
    function new(string name="", uvm_component parent);
        super.new(name, parent);
    endfunction

// ==============================================
// [override] 计算 PLL 期望时钟
    // 从 reg_fields 或 hdl_paths 读取: lock, dsmen, refdiv, fbdiv, frac
    // DSM 关闭: period = pre_period × refdiv / fbdiv
    // DSM 使能: period = pre_period × refdiv / (fbdiv + frac/2^24)
    // PLL 未 lock → UVM_ERROR
// ==============================================
    task get_expe_clk(output real period, output real duty_ratio);
        int     values[string] = '{"lock":0, "dsmen":0, "frac":0, "refdiv":0, "fbdiv":0, "postdiv1":0, "postdiv2":0};

        

        real    pre_period;
        real    pre_duty_ratio;
        uvm_status_e  status;
        int     rdata;

        foreach(values[i])begin
            if(cfg.reg_fields.exists(i))
                cfg.reg_fields[i].read(status, values[i]);
            else
                uvm_hdl_read(cfg.hdl_paths[i], values[i]);
        end


        if(values["lock"] == 1)begin
            cfg.pre_nodes[0].get_expe_clk(pre_period, pre_duty_ratio);
            if(values["dsmen"] == 1'b1)begin
                period = pre_period * values["refdiv"] / (values["fbdiv"] + values["frac"] / 2**24);
            end
            else begin
                period = pre_period * values["refdiv"] / values["fbdiv"];
            end
            if(pre_period != 0)
                duty_ratio = 0.5;
            else
                duty_ratio = 0;
        end
        else begin
            `uvm_error("get_expe_clk", $sformatf("%s not lock", cfg.ci.clk_hire))
        end

        `uvm_info("get_expe_clk", $sformatf("%s:refdiv=%0d, fbdiv=%0d, frac=%0f period=%0f, duty_ratio=%0f",get_name(), values["refdiv"], values["fbdiv"], values["frac"]/real'(2**24), period, duty_ratio), UVM_HIGH)
    endtask

endclass


`endif