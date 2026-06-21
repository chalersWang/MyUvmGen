/***********************************************************
 *  Copyright (C) 2026 by ChalersWang (19910619333@189.cn).
 *  All right reserved.
************************************************************/


// ============================================================================
// 模块名称: svk_crg_if
// 功能概述: 参数化时钟/复位接口容器
//           通过 generate 循环批量实例化 CLK_NUM 个 svk_clk_if 和
//           RST_NUM 个 svk_rst_if，每个 interface 的 clk_hire/rst_hire
//           参数自动赋值为 "0", "1", "2", ...
// 参数:
//   CLK_NUM  — 时钟接口数量 (默认 1)
//   RST_NUM  — 复位接口数量 (默认 1)
// ============================================================================

`ifndef SVK_CRG_IF__SV
`define SVK_CRG_IF__SV

interface svk_crg_if#(int CLK_NUM=1, int RST_NUM=1)();
    logic [CLK_NUM-1:0] clks;
    logic [RST_NUM-1:0] rsts;

    genvar i;

    generate;
       for(i=0; i<CLK_NUM; ++i) 
            svk_clk_if u_clk_if(clks[i], $sformatf("%0d", i));
       for(i=0; i<RST_NUM; ++i) 
            svk_rst_if u_clk_if(clks[i], $sformatf("%0d", i));
    endgenerate
endinterface

`endif
