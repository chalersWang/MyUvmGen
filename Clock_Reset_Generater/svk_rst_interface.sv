/***********************************************************
 *  Copyright (C) 2026 by ChalersWang (19910619333@189.cn).
 *  All right reserved.
************************************************************/



// ============================================================================
// 模块名称: svk_rst_interface (Legacy 版本)
// 功能概述: 旧版复位接口
//           功能与 svk_rst_if 类似，额外提供:
//           - init()             初始化复位序列 (pull_up → delay → pull_down → delay → pull_up)
//           - is_pull_up()       查询复位是否在释放状态 (高电平)
//           - is_pull_down()     查询复位是否在激活状态 (低电平)
//           - wait_pull_up()     等待复位释放 (等 posedge)
//           - wait_pull_down()   等待复位激活 (等 negedge)
//           - is_syn_with(ci)    检测复位与时钟是否同步
// 注意:
//   新项目推荐使用 svk_rst_if + svk_rst_node 体系。
// ============================================================================

`ifndef SVK_RST_INTERFACE__SV
`define SVK_RST_INTERFACE__SV

interface svk_rst_interface(
    inout           rst,
    input string    rst_hire
);

    import uvm_pkg::*;

// ==============================================
// 上拉复位: force rst = 1 (释放复位状态)
// ==============================================
    function void pull_up();
        force rst = 1;
    endfunction

// ==============================================
// 下拉复位: force rst = 0 (激活复位状态)
// ==============================================
    function void pull_down();
        force rst = 0;
    endfunction

// ==============================================
// 释放复位控制: release rst (解除 force, 恢复硬件驱动)
// ==============================================
    function void release_rst();
        release rst;
    endfunction

// ==============================================
// 复位初始化序列
    // 流程: pull_up → wait(pre_rst_time) → pull_down → wait(rst_time) → pull_up
    // 模拟完整芯片上电复位时序
// ==============================================
    task init(real pre_rst_time=0,
              real rst_time = 100);

        fork
            pull_up();
            #(pre_rst_time);
            pull_down();
            #(rst_time);
            pull_up();
            `uvm_info("rst_init", "%s:reset initial is complete!", UVM_NONE)
        join_none
    endtask

// ==============================================
// 查询复位是否在释放状态: rst == 1 → 释放
// ==============================================
    function bit is_pull_up();
        return rst == 1;
    endfunction

// ==============================================
// 查询复位是否在激活状态: rst == 0 → 复位激活中
// ==============================================
    function bit is_pull_down();
        return rst == 0;
    endfunction

// ==============================================
// 阻塞等待复位释放: @(posedge rst)
// ==============================================
    task wait_pull_up();
        @(posedge rst);
        `uvm_info("wait_pull_up", $sformatf("%s pull up", rst_hire), UVM_NONE)
    endtask

// ==============================================
// 阻塞等待复位激活: @(negedge rst)
// ==============================================
    task wait_pull_down();
        @(negedge rst);
        `uvm_info("wait_pull_down", $sformatf("%s pull down", rst_hire), UVM_NONE)
    endtask


// ==============================================
// 检测复位与时钟的同步关系
    // 原理: 比较 posedge rst 与 posedge clk 的时间差
    // |t_rst - t_clk| < th → is_syn=1 (同步), 否则 is_syn=0 (异步)
// ==============================================
    task is_syn_with(virtual svk_clk_interface ci, output bit is_syn, real th = 0);
        realtime    pll_up_time;
        realtime    clk_edge_time;

        wait(rst==1);
        pll_up_time = $realtime();
        wait(ci.clk == 1);
        clk_edge_time = $realtime();

        if(clk_edge_time - pll_up_time < th)
            is_syn = 1;
        else
            is_syn = 0;

    endtask


endinterface
`endif
