/***********************************************************
 *  Copyright (C) 2026 by ChalersWang (19910619333@189.cn).
 *  All right reserved.
************************************************************/


// ============================================================================
// 模块名称: svk_rst_if
// 功能概述: 复位物理接口 (Reset Interface)
//           使用 force 语句物理驱动 DUT 复位线，模拟实际复位行为。
//           支持 configurable up_time (高电平时间) 和 down_time (低电平时间)。
// 接口信号:
//   rst      (inout) — 驱动的复位线
//   rst_hire (input string) — 复位的层级路径名
// 关键参数:
//   up_time   — 复位高电平持续时间 (释放状态)
//   down_time — 复位低电平持续时间 (复位激活状态)
// 关键任务:
//   drive()    — 启动复位驱动: force 1 → #up_time → force 0 → #down_time → force 1
//   undrive()  — 释放复位 (release rst)
//   set_rst()  — 强制设置复位为指定值 (0 或 1)
// ============================================================================

`ifndef SVK_RST_IF__SV
`define SVK_RST_IF__SV

interface svk_rst_if(
    inout           rst,
    input string    rst_hire
);
    real      up_time;
    real      down_time;

    import uvm_pkg::*;

    // 释放复位: release rst, 解除 force 驱动使复位线回到硬件原始状态
    task undrive();
        release rst;
    endtask

    // 驱动复位序列: force 1 → #up_time → force 0 → #down_time → force 1
    // 模拟上电复位波形: 先释放(高), 复位激活(低), 再释放(高)
    task drive();
        force rst = 1;
        #(up_time);
        force rst = 0;
        #(down_time);
        force rst = 1;
    endtask

    // 强制设置复位值为指定值 (0=激活复位, 1=释放复位)
    task set_rst(input logic rst_value);
        force rst = rst_value;
    endtask

endinterface

`endif
